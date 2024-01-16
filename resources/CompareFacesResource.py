from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from flask_restful import Resource
from config import Config
from mysql.connector import Error

from datetime import datetime
from io import BytesIO
import io
import boto3

class CompareFacesResource(Resource) :
    def post(self) :               

        source_file = request.files.get('source_file')
        target_file = request.files.get('target_file')

        if source_file is None or target_file is None :
            return {"error" : '파일을 업로드 하세요'}, 400
        
        face_matches = self.compare_faces(source_file.read(), target_file.read())

        return {'result' : 'success', "items" : face_matches,}, 200
    
    def compare_faces(self, sourceFile, targetFile):

        client = boto3.client('rekognition',
                              'ap-northeast-2',
                              aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)

        imageSource = BytesIO(sourceFile)
        imageTarget = BytesIO(targetFile)

        response = client.compare_faces(SimilarityThreshold=80,
                                        SourceImage={'Bytes': imageSource.read()},
                                        TargetImage={'Bytes': imageTarget.read()})

        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('감지된 얼굴에서 ' +
                str(position['Left']) + ' ' +
                str(position['Top']) +
                ' matches with ' + similarity + '% confidence')

        imageSource.close()
        imageTarget.close()

        return response['FaceMatches']