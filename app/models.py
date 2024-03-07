from sqlalchemy import CheckConstraint, String, Boolean, Integer, Column, text, TIMESTAMP, ARRAY
from databse import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, server_default=text('30') , nullable=False)
    available = Column(Boolean, server_default=text('true'))
    rating = Column(Integer, server_default=text('4'))
    categories = Column(ARRAY(String), nullable=False, server_default='{}')
    imageurl = Column(String, nullable=False, server_default='https://i.imgur.com/crsd3wU.jpeg')
    expectedtime = Column(Integer, nullable=False, server_default=text('5'))

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hostelno = Column(String, nullable=False)
    phoneno = Column(Integer, nullable=False)
    # profile_picture = Column(String, nullable=False)
    # is_active = Column(Boolean, server_default=text('false'))
    last_login = Column(TIMESTAMP(timezone=True), server_default=text('Now()'))

class CurrentOrders(Base):
    __tablename__ = 'current_orders'

    id = Column(Integer, primary_key=True, nullable=False)
    rollno = Column(String, nullable=False)
    items = Column(ARRAY(String), nullable=False, server_default='{}')
    quantity = Column(ARRAY(Integer), nullable=False, server_default='{}')
    total_price = Column(Integer, nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    ### {PREPARAING, READY, DELIVERED}
    status_enum = Column(Integer, nullable=False)

    