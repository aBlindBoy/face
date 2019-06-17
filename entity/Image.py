class Image:
    imageCount = 0

    def __init__(self, image_id, image_path, face_similarity):
        self.image_id = image_id
        self.image_path = image_path
        self.face_similarity = face_similarity
        super().__init__()

    def imageToString(self):
        return "image_id:", self.image_id, "image_path:", self.image_path

    @property
    def convert_to_dict(self):
        '''
        把Object对象转换成Dict对象
        '''
        dict = {}
        dict.update(self.__dict__)
        return dict