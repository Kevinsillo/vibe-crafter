from vibecrafter.domain.models.option_source import OptionSource


def test_parse_pipe_separated_options_returns_list():
    source = OptionSource("Python|TypeScript|Java|Go")
    assert source.static_options() == ["Python", "TypeScript", "Java", "Go"]


def test_is_scan_directive_with_scan_prefix_returns_true():
    source = OptionSource("@scan:designs/|Ninguno")
    assert source.is_scan_directive() is True


def test_is_scan_directive_with_normal_options_returns_false():
    source = OptionSource("Python|TypeScript")
    assert source.is_scan_directive() is False


def test_scan_path_extracts_path_correctly():
    source = OptionSource("@scan:designs/|Ninguno")
    assert source.scan_path() == "designs/"


def test_scan_path_without_directive_returns_none():
    source = OptionSource("A|B|C")
    assert source.scan_path() is None


def test_static_options_excludes_scan_directives():
    source = OptionSource("@scan:designs/|Ninguno")
    assert source.static_options() == ["Ninguno"]
