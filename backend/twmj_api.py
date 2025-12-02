from fastapi import FastAPI

twmj = FastAPI()

@twmj.get("/")
def root():
    return('hello world')