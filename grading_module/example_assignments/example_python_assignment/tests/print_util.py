

def print_calls_contain_output(mock_print, expected_output):

    """ @:param mock_print the mock for builtins.print used to gather info about program's calls
        @:param expected_output a list of strings, in the order expected in the program's output
    """

    # Was print called with the correct statements?

    calls = [str(call[0][0]) for call in mock_print.call_args_list]
    all_output = ''.join(calls)

    cursor = 0

    for out in expected_output:
        cursor = all_output.find(out, cursor)
        if cursor == -1:
            return False, f'Expected to find "{out}" in the program\'s output.'

    return True, ''
