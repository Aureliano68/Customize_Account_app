import os
from uuid import uuid4

# -----------------------------------------------------------------------------------------------------------
class upload_image:
    def __init__(self,dir,prefix):
        self.dir=dir
        self.prefix=prefix
    def upload_to(self,instance,filename):
        filename,ext=os.path.splitext(filename)
        
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'
    
# -----------------------------------------------------------------------------------------------------------
