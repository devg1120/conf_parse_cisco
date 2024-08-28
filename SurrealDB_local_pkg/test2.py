import sys 
sys.path.insert(0,"./surrealdb.py-0.3.2")    

from surrealdb import Surreal
import asyncio

async def test1(db):

   await db.connect()
   await db.signin({"user": "root", "pass": "root"})
   await db.use("test", "test")
   
   # %%
   await db.create(
       "person",
       {
           "user": "me",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   
   # %%
   print(await db.select("person"))
   
   # %%
   await db.update("person", {
       "user":"you",
       "pass":"very_safe",
       "marketing": False,
       "tags": ["Awesome"]
   })
   
   # %%
   await db.delete("person")
   print(await db.select("person"))
   await db.close()

if __name__ == "__main__":

    db = Surreal("ws://localhost:8000/rpc") 
    asyncio.run(test1(db))
