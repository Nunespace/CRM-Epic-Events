from views import menu, get_datas


class TestMenu:
    def test_main_menu(self, mocker):
        mocker.patch("builtins.input", return_value=1)
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.main_menu() == 1

    def test_submenu(self, mocker):
        mocker.patch("builtins.input", return_value=1)
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.submenu("staff") == 1

    def test_view_menu_read_only(self, mocker):
        mocker.patch("builtins.input", return_value=2)
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.view_menu_read_only("event") == 2

    def test_choice_column_to_update(self, mocker):
        mocker.patch("builtins.input", return_value=2)
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.choice_column_to_update("contract") == "total_amount"

    @classmethod
    def teardown_class(cls):
        # This method is being called after each test case, and it will revert input back to original function
        views_menu = menu.Menu()
        views_menu.input = input


class TestGetDatas:

    def test_get_credentials(self, mocker):
        mocker.patch("builtins.input", return_value=("test"))
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_credentials() == ("test", "test")

    def test_get_id_client(self, mocker):
        mocker.patch("builtins.input", return_value="2")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_id("client") == 2
    
    def test_get_id_staff(self, mocker):
        mocker.patch("builtins.input", return_value="4")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_id("staff") == 4

    def test_get_fullname(self, mocker):
        mocker.patch("builtins.input", return_value="dupont dupond")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_name_event() == "Dupont dupond"

    def test_get_name_event(self, mocker):
        mocker.patch("builtins.input", return_value="noël FFF")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_name_event() == "Noël fff"

    def test_check_email(self):
        email = "essai@gmail.com"
        email_checked = get_datas.GetDatas()
        assert email_checked.chek_email(email) == email

    def test_check_id(self):
        id = "4"
        id_checked = get_datas.GetDatas()
        assert id_checked.chek_id(id) == 4

    def test_check_phone(self):
        phone = "0405060514"
        phone_checked = get_datas.GetDatas()
        assert phone_checked.chek_phone(phone) == 405060514

    def test_check_number(self):
        number = "1650"
        number_checked = get_datas.GetDatas()
        assert number_checked.chek_number(number) == 1650

    def test_check_status_true(self):
        status = "1"
        status_checked = get_datas.GetDatas()
        assert status_checked.check_status(status) is True

    def test_check_status_false(self):
        status = "2"
        status_checked = get_datas.GetDatas()
        assert status_checked.check_status(status) is False

    def test_get_new_value(self, mocker):
        mocker.patch("builtins.input", return_value=3)
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_new_value("client_id") == 3

    def test_get_support_contact(self, mocker):
        mocker.patch("builtins.input", return_value="dupont")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_support_contact() == "Dupont"

    def test_get_department(self, mocker):
        mocker.patch("builtins.input", return_value="2")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_department() == "SUPPORT"

    @classmethod
    def teardown_class(cls):
        # This method is being called after each test case, and it will revert input back to original function
        get_datas_test = get_datas.GetDatas()
        get_datas_test.input = input
