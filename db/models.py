from db.base_class import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

# Define the Transactions model
class Transaction(Base):

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer)
    product_name = Column(String)
    amount = Column(Integer)
    type = Column(String)
    time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    

