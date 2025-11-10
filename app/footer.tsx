import { useState } from "react";
import React from "react";


// Define props type
type MemoizedProps = {
  text: string;
}


const Memoizedfunction:React.FC<MemoizedProps> =React.memo(({text})=>{
        console.log("memoized function executed");
        return <div>Memoized Component {text}</div>;
    })

function footer() {
    const [count,setCount]=React.useState(0);
    console.log("Footer function executed");    
    const counter=()=>{
        setCount(prev=>prev+1);
        console.log("count rendered");
    }
    
    

    const data=()=>{
        fetch('/api/getData').then(res=>res.json())
    }
    return(
        <>
        <div>hi</div>
        <div>{count}</div>
        <button onClick={counter}>Increment</button>
        <Memoizedfunction text="hb" />
        </>
    )
}

export default footer;