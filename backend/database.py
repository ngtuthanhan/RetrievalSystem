from model import Video

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
database = client.VideoList
collection = database.video


def import_database(video_list):
    collection.delete_many({})
    collection.insert_many(video_list)

async def fetch_one_video(keyframe):
    document = await collection.find_one({"keyframe": keyframe})
    return document

async def fetch_all_video():
    videos = []
    cursor = collection.find({})
    async for document in cursor:
        videos.append(Video(**document))
    return videos

async def create_video(video):
    document = video
    result = await collection.insert_one(document)
    return result

async def update_video(keyframe, video):
    await collection.update_one({"keyframe": keyframe}, 
                                {"$set": video})
    document = await collection.find_one({"keyframe": keyframe})
    return document

async def remove_video(keyframe):
    await collection.delete_one({"keyframe": keyframe})
    return True
            