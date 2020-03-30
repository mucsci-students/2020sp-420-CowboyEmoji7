from app_package import db
from app_package.models import Class, ClassSchema, Relationship, Attribute, RelationshipSchema, AttributeSchema, Theme, ThemeSchema
from os import listdir
from os.path import isfile, join

def populateThemes():
    """
    Populates themes database with all theme names and sets default
    """
    themePath = "app_package/static/css/themes"
    themeNames = [f for f in listdir(themePath) if isfile(join(themePath, f))]
    for theme in themeNames:
        #Setting default theme
        nameFormatted = theme[:-4]
        if (nameFormatted == 'Dark-Green'):
            newTheme = Theme(name=nameFormatted, active=True)
        else:
            newTheme = Theme(name=nameFormatted, active=False)
        db.session.add(newTheme)
        
        
db.drop_all()
db.create_all()
populateThemes()

db.session.commit()

