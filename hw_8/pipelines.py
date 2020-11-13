# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class NewParsPipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client['geekbrain']

    def process_item(self, item, spider):
        follower = item["user"]
        del_user = []
        for user in item["data"]:
            if user != follower:
                del_user.append(user)
        for user in del_user:
            item["data"].pop(user)
        if "connection" not in item["data"][follower]:
            item["data"][follower]["connection"] = []
        try:
            for user in item["data"][follower]["followers"]:
                if user in item["data"][follower]["following"]:
                    item["data"][follower]["connection"].append(user)
            item["data"][follower].pop("following")
            item["data"][follower].pop("followers")
            collection = self.db[type(item).__name__]
            my_list = []
            for i in collection.find({}):
                my_list.append(i["user"])
            if follower not in my_list:
                collection.insert_one(item)
            print('pipelines')
            return item
        except KeyError as e:
            print(e)


class AnalysisPipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client['geekbrain']
        self.start_user = "royalty_beauty_space"
        self.finish_user = "kenichi_arai"

    def process_item(self, item, spider):
        collection = self.db[type(item).__name__]
        a = collection.find({})
        analysis_dict = {}
        for i in a:
            user = i["user"]
            analysis_dict[user] = i["data"][user]["connection"]

        keep_going = True
        while keep_going:
            if self.start_user and self.finish_user in analysis_dict:
                for i in analysis_dict:
                    if i != self.finish_user:
                        if i == self.start_user:
                            for j in analysis_dict[i]:
                                if j in analysis_dict[self.finish_user]:
                                    print(f'You got connection by one hand shake by user {j} hand')
                                    keep_going = False
                                    break
                        else:
                            if i != self.finish_user and i != self.start_user:
                                for j in analysis_dict[i]:
                                    if j in analysis_dict[self.start_user] and j in analysis_dict[self.finish_user]:
                                        print(f'You got connection by shake by user {i} and user {j} hands')
                                        keep_going = False
                                        break
                                    if j in analysis_dict[self.start_user] and j != self.start_user:
                                        if j in analysis_dict:
                                            for k in analysis_dict[j]:
                                                if k in analysis_dict[self.finish_user]:
                                                    print(f"You got connection by shake by users {i} ,{j},{k}  hands")
                                                    keep_going = False
                                                    break
                                                else:
                                                    if k in analysis_dict:
                                                        for l in analysis_dict[k]:
                                                            if l in analysis_dict[self.finish_user]:
                                                                print(
                                                                    f"You got connection by shake by users {i} ,{j},{k}, {l}  hands")
                                                                keep_going = False
                                                                break
                                                            else:
                                                                if l in analysis_dict:
                                                                    for m in analysis_dict[l]:
                                                                        if m in analysis_dict[self.finish_user]:
                                                                            print(
                                                                                f"You got connection by shake by users {i} ,{j},{k}, {l}, {m}  hands")
                                                                            keep_going = False
                                                                            break
                                                                        else:
                                                                            if m in analysis_dict:
                                                                                for n in analysis_dict[m]:
                                                                                    if m in analysis_dict[
                                                                                        self.finish_user]:
                                                                                        print(
                                                                                            f"You got connection by shake by users {i} ,{j},{k}, {l}, {m}, {n}  hands")
                                                                                    keep_going = False
                                                                                    break
                                                                            else:
                                                                                print(
                                                                                    f"{j} in not in analysis dict yet")


                                                                else:
                                                                    print(f"{l} in not in analysis dict yet")

                                                    else:
                                                        print(f"{k} in not in analysis dict yet")

                                        else:
                                            print(f"{j} in not in analysis dict yet")
            keep_going = False

# class NewParsImagesPipeline(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         images = item.get('img',
#                           item.get('data', {}).get('profile_pic_url',
#                                                    item.get('data', {}).get('display_url',
#                                                                             []
#                                                                             )
#                                                    )
#                           )
#
#         if not isinstance(images, list):
#             images = [images]
#         for url in images:
#             try:
#                 yield Request(url)
#             except Exception as e:
#                 print(e)
#
#     def item_completed(self, results, item, info):
#         try:
#             item['img'] = [itm[1] for itm in results if itm[0]]
#         except KeyError:
#             pass
#         return item
