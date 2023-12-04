from controllers.login_manager import AuthenticationAndPermissions
from settings import Base, ENGINE


def main():
    Base.metadata.create_all(ENGINE)
    run = AuthenticationAndPermissions()
    run.check_password()


if __name__ == "__main__":
    main()
