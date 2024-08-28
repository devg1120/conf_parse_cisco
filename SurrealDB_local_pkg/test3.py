import sys 
sys.path.insert(0,"./surrealdb.py-0.3.2")    

from surrealdb import Surreal
import asyncio
import datetime

async def test1(db):
   print("---------------------- test1")
   await db.delete("person")
   await db.create(
       "person",
       {
           "user": "me",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   
   await db.create(
       "person",
       {
           "user": "me",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   
   await db.update("person", {
       "user":"you",
       "pass":"very_safe",
       "marketing": False,
       "tags": ["Awesome"]
   })
   
   results = await db.select("person")
   for record in results:
       print(record)
   await db.delete("person")

async def test12(db):
   print("---------------------- test12")
   await db.delete("person")
   await db.create(
       "person",
       {
           "id": "test001",
           "user": "me",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   
   await db.create(
       "person",
       {
           "id": "test002",
           "user": "me",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   
   await db.update("person:test002", {
       "user":"you",
       "pass":"very_safe",
       "marketing": False,
       "tags": ["Awesome"]
   })
   
   #await db.merge("person:test002", {
   #    "user2":"gs",
   #})
   results = await db.select("person")
   for record in results:
       print(record)
   await db.delete("person")
async def test2(db):
   print("---------------------- test2")
   await db.let("name", {
             "first": "Tobie",
             "last": "Morgan Hitchcock",
         })
   print(await db.query('CREATE person SET name = $name'))
   print(await db.query('SELECT * FROM person WHERE name.first = $name.first'))
   print(await db.query('DELETE person'))
   print(await db.query('SELECT * FROM person'))
   print(await db.query('SELECT * FROM person WHERE name.first = $name.first'))

async def test3(db):
   # record id  auto
   print("---------------------- test3")
   await db.delete("person")
   await db.query("""
        insert into person {
            user: 'me',
            pass: 'very_safe',
            tags: ['python', 'documentation']
        };
        
        """)
   await db.query("""
        insert into person {
            user: 'me',
            pass: 'very_safe',
            tags: ['python', 'documentation']
        };
        
        """)
   results = await db.select("person")
   for record in results:
       print(record)

   await db.query("""
        update person content {
            user: 'you',
            pass: 'more_safe',
            tags: ['awesome']
        };
        
        """)
   print("")
   results = await db.select("person")
   for record in results:
       print(record)

async def test4(db):
   # record id  set
   print("---------------------- test4")
   await db.delete("person")
   await db.query("""
        insert into person {
            id: "tobie1",
            user: 'me',
            pass: 'very_safe',
            tags: ['python', 'documentation']
        };
        
        """)
   await db.query("""
        insert into person {
            id: "tobie2",
            user: 'me',
            pass: 'very_safe',
            tags: ['python', 'documentation']
        };
        
        """)
   results = await db.select("person")
   for record in results:
       print(record)

   await db.query("""
        update person:tobie2 content {
            user: 'you',
            pass: 'more_safe',
            tags: ['awesome']
        };
        
        """)
   print("")
   results = await db.select("person")
   for record in results:
       print(record)

async def test5(db):
   print("---------------------- test4")
   await db.delete("person")
   await db.create(
           "person:tobie1",
       {
           "user": "me1",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   await db.create(
           "person:tobie2",
       {
           "user": "me2",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )

   await db.create(
           "person:tobie3",
       {
           "user": "me3",
           "pass": "safe",
           "marketing": True,
           "tags": ["python", "documentation"],
       },
   )
   results = await db.select("person")
   for record in results:
       print(record)
   
   await db.update('person:tobie3', {
           "user": "me3",
           "pass": "safe",
           "marketing": False,
           "tags": ["python", "documentation"],
   })
   print("")
   results = await db.select("person")
   for record in results:
       print(record)

   
   await db.delete("person")



async def main():
   db = Surreal("ws://localhost:8000/rpc") 
   #db = AsyncSurrealDB("ws://localhost:8000/rpc") 
   await db.connect()
   await db.signin({"user": "root", "pass": "root"})
   await db.use("ns_test", "db_test")

   #await test11(db)    # api (create,select,update)
   await test12(db)    # api (create,select,update)
   #await test2(db)    # query  create
   #await test3(db)    # query  insert  / auto id
   #await test4(db)   # query  insert  / set id
   #await test5(db)

   await db.close()

if __name__ == "__main__":
   asyncio.run(main())
