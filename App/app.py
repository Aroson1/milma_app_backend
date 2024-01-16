# Google client authentication API from: https://console.cloud.google.com/apis/credentials
from firebase_admin import credentials, auth
import firebase_admin
import pyrebase
import uvicorn

from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from oauthlib.oauth2 import WebApplicationClient
from dotenv import load_dotenv
import os
import requests
import json

# Firebase configuration and initialization
load_dotenv()
cred = credentials.Certificate(
    json.loads(os.environ["FIREBASE_ADMIN_CONFIG"])
)
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.loads(os.environ["FIREBASE_CONFIG"]))


# FastAPI set-up and configuration
app = FastAPI()
allow_all = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)


# Google OAuth Configuration
GOOGLE_CLIENT_ID = (
    os.environ["GOOGLE_CLIENT_ID"]
)
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# IMP: MUST BE COMMENTED OUT WHEN IN NOT IN TESTING
# ----------------------------------------------
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# ----------------------------------------------


# Google sign-in endpoint
@app.get("/google-auth")
async def google_sign_in(req: Request):
    redirect_URL = req.base_url._url + "google-auth/callback"

    # Getting the URL for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Setting up request body and scope to retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_URL,
        scope=["openid", "email", "profile"],
    )

    # Redirect user to google sign-in page
    return RedirectResponse(request_uri)


# The google sign-in redirects to this endpoint
@app.route("/google-auth/callback")
def callback(req: Request, **param_list):
    # Get authorization code Google sent back
    code = req.query_params["code"]

    # Get the compelete url with the params list sent back by Google
    auth_URL = req.url._url

    # Get the base url of the host
    # [For testing base_url = http://127.0.0.1:1234/login/callback]
    redirect_URL = req.base_url._url + "google-auth/callback"

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=auth_URL,
        redirect_url=redirect_URL,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get user details from the response token
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Check if user is verified
    if userinfo_response.json().get("email_verified"):
        user = userinfo_response.json()
        unique_id = user["sub"]
        users_email = user["email"]
        picture = user["picture"]
        users_name = user["given_name"]

        if validate(users_email):
            # ---------------------------------------------------------------------------
            # Get nessasary data on the user from database and return it to app
            # ---------------------------------------------------------------------------
            return JSONResponse(
                content={"message": "User loggedin", "user": users_name},
                status_code=200,
            )
            
        else:
            # Create a new user in firebase
            try:
                user = auth.create_user(email=users_email, password=unique_id)

                # ---------------------------------------------------------------------------
                # Additional code for adding to database
                # ---------------------------------------------------------------------------

                return JSONResponse(
                    content={"message": f"Successfully created user {users_name}"},
                    status_code=200,
                )
            except:
                return HTTPException(
                    detail={"message": "Couldn't create a account"}, status_code=400
                )

    else:
        return JSONResponse(
            content={"message": "User email not available or not verified by Google."},
            status_code=400,
        )


# Email signup endpoint
@app.post("/email-signup")
async def signup(req: Request):
    req = await req.json()
    email = req["email"]
    password = req["password"]
    if email is None or password is None:
        return HTTPException(
            detail={"message": "Error! Missing Email or Password"}, status_code=400
        )
    try:
        # Create user using firebase admin
        user = auth.create_user(email=email, password=password)

        # ---------------------------------------------------------------------------
        # Additional code for adding to database
        # ---------------------------------------------------------------------------

        return JSONResponse(
            content={"message": f"Successfully created user {user.uid}"},
            status_code=200,
        )
    except:
        return HTTPException(detail={"message": "Error Creating User. User already exists."}, status_code=400)


# Email login endpoint
@app.post("/email-login")
async def login(req: Request):
    req_json = await req.json()
    email = req_json["email"]
    password = req_json["password"]
    try:
        # sign-in user with pyrebase and store the JWT token
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user["idToken"]
        # ---------------------------------------------------------------------------
        # Additional code for adding to database
        # ---------------------------------------------------------------------------

        return JSONResponse(content={'token': jwt}, status_code=200)

    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

# DEBUG-ENDPOINT: ping endpoint for validating JWT token
@app.post("/ping", include_in_schema=False)
async def vali(req: Request):
    headers = req.headers
    jwt = headers.get("authorization")
    print(f"jwt:{jwt}")
    user = auth.verify_id_token(jwt)
    return user["uid"]

def validate(email):
    try:
        auth.get_user_by_email(email)
        return True
    except:
        return False


def get_google_provider_cfg():
    try:
        req = requests.get(GOOGLE_DISCOVERY_URL).json()
        return req
    except:
        return JSONResponse(
            content={"message": "Getting Google_discovery_url Failed"}, status_code=400
        )



if __name__ == "__main__":
    uvicorn.run("app:app")