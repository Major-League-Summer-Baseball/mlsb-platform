MLSB Basic APIs
=========
#Bat APIs
ALL Basic APIs have same format for their response
```sh
JSON
{  
   "data":data,
   "failures":Array,
   "message":String,
   "success":Boolean
}
```
## ```Bat GET bats/bat_id``` 
This api gets a bat object

##### Response Data:
JSON (Bat Object) : 
```sh
{  
   "bat_id":1,
   "classification":"HR",
   "game_id":1,
   "player_id":1,
   "rbi":4
}
```
```
## ```Bat GET bats``` 
This api gets all bat objects

##### Response Data:
JSON (Bat Object) : 
```sh
[  
   {  
      "bat_id":1,
      "classification":"HR",
      "game_id":1,
      "player_id":1,
      "rbi":4
   }
]
```
