def replace_all_punc(s):
    pm_set = {".", ",", ":", "?", "!", "(", ")", "\n"}
    for pm in pm_set:
        s = s.replace(pm, "")
    return s
# на будущее: сделать возможность указывать, какие именно символы не нужно удалять


def all_punc_to_whitespases(s):
    pm_set = {".", ",", ":", "?", "!", "(", ")", "\n"}
    for pm in pm_set:
        s = s.replace(pm, " ")
    return s


def yes_or_no(p_bool):
    return "YES" if p_bool else "NO"


FORBIDDING_WORDS = {'0', 'false', 'no', 'not'}


def are_forbidding_words_here(string):
    for fw in FORBIDDING_WORDS:
        if fw in string:
            return True
    return False
