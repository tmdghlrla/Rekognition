from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.CompareFacesResource import CompareFacesResource
from resources.RecognizeFacesResource import RecognizeFacesResource

app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)

# JWT 매니저 초기화
jwt=JWTManager(app)

api = Api(app)

# 경로와 리소스를 연결한다.
api.add_resource(CompareFacesResource,'/compare')
api.add_resource(RecognizeFacesResource,'/recognize')

if __name__ == '__main__' :
    app.run()