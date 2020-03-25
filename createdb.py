from app_package import db
from app_package.models import Class, ClassSchema, Relationship, Attribute, RelationshipSchema, AttributeSchema, Theme, ThemeSchema
from os import listdir
from os.path import isfile, join

themePath = "app_package/static/css/themes"

db.drop_all()
db.create_all()

themeNames = [f for f in listdir(themePath) if isfile(join(themePath, f))]
for theme in themeNames:
    #Setting default theme
    if (theme == 'Dark-Green.css'):
        newTheme = Theme(name=theme, active=True)
    else:
        newTheme = Theme(name=theme, active=False)
    db.session.add(newTheme)

db.session.commit()

