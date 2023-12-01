from controllers.login_manager import AuthenticationAndPermissions
from settings import Base, ENGINE
from rich import pretty


def main():
    Base.metadata.create_all(ENGINE)
    run = AuthenticationAndPermissions()
    pretty.install()
    run.check_password()


if __name__ == "__main__":
    main()
