

from views import menu, get_datas


class TestMenu:

    def test_main_menu(self, mocker):
        mocker.patch("builtins.input", return_value=1)
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.main_menu() == 1

    def teardown_method(self, test_main_menu):
        # This method is being called after each test case, and it will revert input back to original function
        main_menu = menu.Menu()
        main_menu.input = input


class TestGetDatas:
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

