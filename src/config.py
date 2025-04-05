import src.color as color

def test_name(index: int):
    return f"test{index}.txt"

def index_from_test(name):
    return int(name.removesuffix('.txt').removeprefix('test'))

def status(proc_code, check_code, time, timeout):
    if proc_code != 0:
        if (time >= timeout):
            return TestStatus.TL
        return TestStatus.RE
    if check_code != 0:
        return TestStatus.WA
    return TestStatus.OK

class TestStatus:
    OK = 'OK'
    WA = 'WA'
    RE = 'RE'
    TL = 'TL'
    @staticmethod
    def is_ok(status):
        return status == TestStatus.OK
    
def print_test_info(name, status, time):
    print(name, end='\t')
    if TestStatus.is_ok(status):
        color.mark_info()
    else:
        color.mark_error()
    print(status, end='\t')
    color.clear_marks()
    print(f"{time:.6f}s", end='\t')
    print()

def print_additional_data(name, data):
    color.mark_yellow()
    print(name)
    color.clear_marks()
    print(data)