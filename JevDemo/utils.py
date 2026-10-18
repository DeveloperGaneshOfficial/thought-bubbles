import pickle

def saveResult(res):
    with open("need_tool.pkl", "wb") as f:
        pickle.dump(res, f)