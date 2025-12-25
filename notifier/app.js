const Redis = require("ioredis");


const redis = new Redis({
  host: '127.0.0.1',
  port: 6379,
  db: 1 
})


console.log("wait for conect to redis");

redis.subscribe("cart_notification",(err,count)=>{
    if (err)console.error("ERROR",err);
    console.log(`subscribe in ${count}` );
})

redis.on("message",(channel,message)=>{
    const data = JSON.parse(message);

    if (data.event === 'item_added') {
        console.log(` user: ${data.user_id} add ${data.product_id} to cart .`);
    } else if (data.event === 'item_removed') {
        console.log(`  user: ${data.user_id}  removed: ${data.product_id} from cart `);
    }
})
