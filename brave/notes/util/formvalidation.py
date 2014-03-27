from web import form

id_validator = form.Validator('ID not valid.', lambda x:len(x)==24)
catid_validator = form.Validator('Category ID not valid.', lambda x:len(x)==24)
title_validator = form.Validator('Title needs be between 1-19 characters', lambda x:len(x.strip())>0 and len(x) <= 19)
name_validator = form.Validator('Title needs be between 1-14 characters', lambda x:len(x.strip())>0 and len(x) <= 14)
body_validator = form.Validator('Body may not be empty', lambda x:len(x.strip())>0)