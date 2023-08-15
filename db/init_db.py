from models import *


if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:123@localhost/")
    engine.connect()
    AuthBase.metadata.create_all(engine)

    print('Auth table succesfully created')
