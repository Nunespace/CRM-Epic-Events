from models.models import Client, Staff, Contract
from controllers.crud_manager import CrudManager
from settings import SESSION
from controllers import login_manager, menu_manager, permissions

FAKE_PASSWORD = "12345"
FAKE_HASHED_PASSWORD = (
    "$argon2id$v=19$m=65536,t=3,p=4$AcB4D8GYc27tnRPinNM6hw$2PfVv4W"
    "H1CoD0/TWmyDw2z0iBTj++WAVt/G9IJRnvtg"
)


class TestLogin:
    def test_check_password(self, mocker):
        mocker.patch("controllers.login_manager.Menu")
        mocker.patch("controllers.login_manager.Messages")
        MockGetDatas = mocker.patch("controllers.login_manager.GetDatas")
        MockGetDatas.return_value.get_credentials.return_value = (
            "me@example.com",
            FAKE_PASSWORD,
        )

        mock_session = mocker.patch("controllers.login_manager.SESSION")
        mock_staff_user = (
            mock_session.query.return_value.filter.return_value.one_or_none.return_value
        )
        mock_staff_user.password = FAKE_HASHED_PASSWORD
        mock_staff_user.department.name = "COMMERCIAL"
        mock_create_token = mocker.patch(
            "controllers.login_manager.AuthenticationAndPermissions.create_token"
        )
        MockMenuManager = mocker.patch("controllers.login_manager.MenuManager")
        mock_choice_main_menu = MockMenuManager.return_value.choice_main_menu

        auth_and_perms = login_manager.AuthenticationAndPermissions()
        auth_and_perms.check_password()

        # -tc- On vérifie que create_token est appelé avec les bons arguments
        mock_create_token.assert_called_once_with("COMMERCIAL")
        # -tc- On vérifie que choice_main_menu est appelé une fois et sans args
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()


class TestCrud:
    def test_create_client_ok(
        self,
        mocker,
        get_datas_create_client_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_client_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("client") == "creation_ok"

    def test_create_client_false(
        self,
        mocker,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value="bad_datas",
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("client") is False

    def test_create_contract_ok(
        self,
        mocker,
        get_datas_create_contract_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_contract_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("contract") == "creation_ok"

    def test_create_contract_with_unknown_client(
        self,
        mocker,
        get_datas_create_contract_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        get_datas_create_contract_fixture["client_id"] = 999
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_contract_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("contract") == "unknown_client"

    def test_create_staff_ok(
        self,
        mocker,
        get_datas_create_staff_fixture,
        staff_user_management_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_staff_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.create("staff") == "creation_ok"

    def test_create_staff_not_allowed(
        self,
        mocker,
        get_datas_create_staff_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_staff_fixture,
        )

        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("staff") == "not_allowed"

    def test_read_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("client") is True

    def test_read_contract_ok(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=2)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("contract") is True

    def test_read_contract_with_unknown_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=2)
        mocker.patch(
            "views.get_datas.GetDatas.get_fullname",
            return_value="unknown client",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("contract") is False

    def test_read_contract_with_unknown_event(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=4)
        mocker.patch(
            "views.get_datas.GetDatas.get_name_event",
            return_value="unknown event",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("contract") is False

    def test_read_event_ok(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("event") is True

    def test_read_event_not_exist(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=2)
        mocker.patch(
            "views.get_datas.GetDatas.get_name_event",
            return_value="event that doesn't exist",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("event") is False

    def test_read_event_with_no_existent_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=4)
        mocker.patch(
            "views.get_datas.GetDatas.get_fullname",
            return_value="client that doesn't exist",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("event") is False

    def test_read_staff_ok(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=2)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("staff") is True

    def test_read_staff_with_name_and_first_name_not_exist(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch(
            "views.get_datas.GetDatas.get_name_and_first_name_staff",
            return_value=(
                "name that doesn't exist",
                "first name that doesn't exist",
            ),
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("staff") is False

    def test_read_staff_with_email_not_exist(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=4)
        mocker.patch(
            "views.get_datas.GetDatas.get_email",
            return_value="unknown@email.com",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("staff") is False

    def test_update_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_fullname",
            return_value="Cyril Dupont",
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_update",
            return_value=True,
        )
        mocker.patch("views.menu.Menu.choice_column_to_update", return_value=1)
        mocker.patch(
            "views.get_datas.GetDatas.get_new_value",
            return_value="Henri Dupond",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.update("client") == "update_ok"

    def test_update_contract(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=2)
        mocker.patch(
            "controllers.permissions.Permissions.permission_update",
            return_value=True,
        )
        # column_to_update = 1 = id du client
        mocker.patch("views.menu.Menu.choice_column_to_update", return_value=1)
        mocker.patch("views.get_datas.GetDatas.get_new_value", return_value=3)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.update("contract") == "update_ok"

    def test_update_event(
        self, mocker, staff_user_management_and_token_fixture
    ):
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        mocker.patch(
            "controllers.permissions.Permissions.permission_update",
            return_value=True,
        )
        # column_to_update = 3 = id du client
        # mocker.patch("views.menu.Menu.choice_column_to_update", return_value=3)
        mocker.patch(
            "views.get_datas.GetDatas.get_support_contact", return_value=3
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.update("event") == "update_ok"

    def test_update_staff(
        self, mocker, staff_user_management_and_token_fixture
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_name_and_first_name_staff",
            return_value=("Henry", "Thierry"),
        )
        mocker.patch("views.menu.Menu.choice_column_to_update", return_value=3)
        mocker.patch(
            "views.get_datas.GetDatas.get_new_value",
            return_value="nouvel_email@gmail.com",
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.update("staff") == "update_ok"

    @classmethod
    def teardown_class(cls):
        client = (
            SESSION.query(Client)
            .filter(Client.fullname == "Cyril Dupont")
            .first()
        )
        if client is not None:
            SESSION.delete(client)
        contract = (
            SESSION.query(Contract).filter(Contract.client_id == 1).first()
        )
        if contract is not None:
            SESSION.delete(contract)

        staff = SESSION.query(Staff).filter(Staff.name == "Gandriau").first()
        if staff is not None:
            SESSION.delete(staff)

        contract_update = (
            SESSION.query(Contract).filter(Contract.id == 2).first()
        )
        contract_update.client_id = 2
        try:
            SESSION.commit()
        except:
            SESSION.rollback()
            raise
        finally:
            SESSION.close()


class TestMenuManager:
    def test_main_menu(self, mocker, staff_user_commercial_and_token_fixture):
        mocker.patch("views.menu.Menu.main_menu", return_value=1)
        mock_choice_submenu = mocker.patch(
            "controllers.menu_manager.MenuManager.choice_submenu"
        )
        choice_submenu = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_submenu.choice_main_menu()
        mock_choice_submenu.assert_called_once()
        mock_choice_submenu.assert_called_once_with("client")

    def test_choice_submenu(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.submenu", return_value=2)
        mocker.patch(
            "controllers.crud_manager.CrudManager.create",
            return_value="creation_ok",
        )
        mock_message_ok = mocker.patch("views.messages.Messages.messages_ok")
        mock_message_ok.return_value = "Le client a bien été enregistré."
        # print(f"message de confirmation : {mock_message_ok}")
        mock_choice_main_menu = mocker.patch(
            "controllers.login_manager.MenuManager.choice_main_menu"
        )
        choice_crud_create = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_crud_create.choice_submenu("client")
        mock_message_ok.assert_called_once_with("client", 1)
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()

    def test_choice_submenu_with_message_error(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        # option 3 = modifier
        mocker.patch("views.menu.Menu.submenu", return_value=3)
        mocker.patch(
            "controllers.crud_manager.CrudManager.update",
            return_value="error",
        )
        mock_message_error = mocker.patch("views.messages.Messages.message_error")
        mock_message_error.return_value = "Une erreur s'est produite. Veuillez recommencer."
        mock_choice_main_menu = mocker.patch(
            "controllers.login_manager.MenuManager.choice_main_menu"
        )
        choice_crud_update = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_crud_update.choice_submenu("client")
        mock_message_error.assert_called_once_with("client", 3)
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()

    def test_choice_submenu_with_message_erro_not_allowed(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        # option 3 = modifier
        mocker.patch("views.menu.Menu.submenu", return_value=3)
        mocker.patch(
            "controllers.crud_manager.CrudManager.update",
            return_value="not_allowed",
        )
        mock_message_error = mocker.patch("views.messages.Messages.message_error")
        mock_message_error.return_value = "Vous n'êtes pas autorisé(e) à effectuer cette action."
        mock_choice_main_menu = mocker.patch(
            "controllers.login_manager.MenuManager.choice_main_menu"
        )
        choice_crud_update = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_crud_update.choice_submenu("client")
        mock_message_error.assert_called_once_with("client", 5)
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()


class TestPermissions:
    def test_check_token_validity_with(self, mocker):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDExOTQ2NjEsImRlcGFydG1lbnQiOiJDT01NRVJDSUFMIn0.skKnyJwwNUh4QdClbJ5OvVaWtbxpEFRXA7ufDcjrKZk"
        mock_message_error = mocker.patch(
            "views.messages.Messages.message_error"
        )
        mock_message_error.return_value = "Veuillez fermer l'application et vous authentifier de nouveau avec la commande : 'pipenv run python main.py'"
        # with pytest.raises(ExpiredSignatureError):
        check_token = permissions.Permissions()
        assert check_token.check_token_validity(token) is False
        # mock_message_error.assert_called_once_with("client", 2)

    def test_permission_create_client(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "COMMERCIAL"},
        )
        perm_create = permissions.Permissions()
        assert perm_create.permission_create("token", "client") is True

    def test_permission_create_staff(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "MANAGEMENT"},
        )
        perm_create = permissions.Permissions()
        assert perm_create.permission_create("token", "staff") is True

    def test_permission_update_client(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "COMMERCIAL"},
        )
        perm_update = permissions.Permissions()
        assert perm_update.permission_update(1, 1, "token", "client") is True

    def test_permission_update_event(self, mocker):
        # un collaborateur Support peut modifier les événements dont il est responsable
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "SUPPORT"},
        )
        perm_update = permissions.Permissions()
        assert perm_update.permission_update(3, 4, "token", "event") is True

    def test_is_own_client(self, mocker):
        own_client = permissions.Permissions()
        assert own_client.is_own_client(1, 1) is True

    def test_is_their_event(self):
        their_event = permissions.Permissions()
        assert their_event.is_their_event(3, 4) is True
