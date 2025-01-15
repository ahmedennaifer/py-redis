from src.parse import parse_command, parse_sub_command, Command, CommandResult


class CommandConfig:
    get_query = "GET Hello"
    set_query = "SET Hello World"
    del_query = "DEL Hello"


class SubCommandConfig:
    get_subc = "Hello"
    set_subc_str = "Hello World"
    set_subc_str_int = "Hello 1"
    set_subc_int_str = "1 Hello"


def test_parse_get():
    res = parse_command(CommandConfig.get_query)
    assert res == CommandResult(Command.GET, "Hello", None)


def test_parse_set():
    res = parse_command(CommandConfig.set_query)
    assert res == CommandResult(Command.SET, "Hello", "World")


def test_parse_del():
    res = parse_command(CommandConfig.del_query)
    assert res == CommandResult(Command.DEL, "Hello", None)


def test_parse_sub_command():
    res = parse_sub_command(SubCommandConfig.get_subc)
    assert res == ("Hello", None)


def test_parse_sub_command_str():
    res = parse_sub_command(SubCommandConfig.set_subc_str)
    assert res == ("Hello", "World")


def test_parse_sub_command_str_int():
    res = parse_sub_command(SubCommandConfig.set_subc_str_int)
    assert res == ("Hello", "1")


def test_parse_sub_command_int_str():
    res = parse_sub_command(SubCommandConfig.set_subc_int_str)
    assert res == ("1", "Hello")
