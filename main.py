from controllers.login_manager import AuthenticationAndPermissions
from views.login import ViewLogin


def main():
    #Base.metadata.create_all(engine)
    run = AuthenticationAndPermissions()
    run.check_password()


if __name__ == "__main__":
    main()

