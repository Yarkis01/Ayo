

def check_ds_code(code: str) -> bool:
    if len(code) != 12 and len(code) != 14:
        return False

    if len(code) == 14:
        split = code.split("-")
    else:
        split = [code[:4], code[4:8], code[8:12]]

    if len(split) != 3:
        return False
    if len(split[0]) != 4 or len(split[1]) != 4 or len(split[2]) != 4:
        return False
    if not split[0].isdigit() or not split[1].isdigit() or not split[2].isdigit():
        return False

    return True

def format_ds_code(code: str) -> str:
    if len(code) == 12:
        code = code[:4] + "-" + code[4:8] + "-" + code[8:12]
    return code



def check_switch_code(code: str) -> bool:
    code = code.lower().replace("sw-", "")
    return check_ds_code(code)

def format_switch_code(code: str) -> str:
    code = code.lower().replace("sw-", "")
    return "SW-" + format_ds_code(code)



def check_home_code(code: str) -> bool:
    if len(code) != 12:
        return False
    
    if not code.isalpha():
        return False

    return True

def format_home_code(code: str) -> str:
    return code.upper()




def check_master_code(code: str) -> bool:
    if len(code) != 16 and len(code) != 19:
        return False

    if len(code) == 19:
        split = code.split("-")
    else:
        split = [code[:4], code[4:8], code[8:12], code[12:16]]

    if len(split) != 4:
        return False
    if len(split[0]) != 4 or len(split[1]) != 4 or len(split[2]) != 4 or len(split[3]) != 4:
        return False
    if not split[0].isdigit() or not split[1].isdigit() or not split[2].isdigit() or not split[3].isdigit():
        return False

    return True

def format_master_code(code: str) -> str:
    if len(code) == 16:
        code = code[:4] + "-" + code[4:8] + "-" + code[8:12] + "-" + code[12:16]
    return code



def check_shuffle_code(code: str) -> bool:
    if len(code) != 8:
        return False

    if not code.isalnum():
        return False

    return True

def format_shuffle_code(code: str) -> str:
    return code.upper()



def check_cafemix_code(code: str) -> bool:
    if len(code) != 12 and len(code) != 14:
        return False

    if len(code) == 14:
        split = code.split("-")
    else:
        split = [code[:4], code[4:8], code[8:12]]

    if len(split) != 3:
        return False
    if len(split[0]) != 4 or len(split[1]) != 4 or len(split[2]) != 4:
        return False
    if not split[0].isalnum() or not split[1].isalnum() or not split[2].isalnum():
        return False

    return True

def format_cafemix_code(code: str) -> str:
    if len(code) == 12:
        code = code[:4] + "-" + code[4:8] + "-" + code[8:12]
    return code.upper()