var num = 0;
    function updateNum(){
        ReactDOM.render(
            <div>{num++}</div>,
            document.getElementById("root")
        )
    }
    setInterval(updateNum,100);

    //////////////////////
    var styleObject = {
    backgroundColor: 'red',
    color:'blue',
    fontSize: 25,
    width: 100
}
    var element2 = <input style = {styleObject}/>
    ReactDOM.render(
        element2,
        document.getElementById("root2")
    )

    ////////////////////////
    var element3 = (
    <div>
        <div>Hello World</div>
        <div>Hello World</div>
    </div>
)
    ReactDOM.render(
        element3,
        document.getElementById("root3")
    )

    ////////////////////////
    function Element(props){
        return (<div> Item: {props.item} | Total: {props.cost * props.quantity} </div> );
    }
    ReactDOM.render(
        <Element item = "cheese" cost = {3} quantity = {10} totalCost = {50}/>,
        document.getElementById("root4")
    )

    ////////////////////////
    function Feature(props){
        return <h1>{props.active && (props.loggedIn? "Welcome!" : "Please Log In")} </h1>
    }
    ReactDOM.render(
        <Feature active = {false} loggedIn = {true}/>,
        document.getElementById("root5")
    )

    ////////////////////////
    function Feature2(props){
        return <h1>Message: {props.message + '!'} {props.userArray[props.userId + 1]} </h1>
    }
ReactDOM.render(
    <Feature2 message = "Welcome" userId = {1} userArray={['Bob','Joe','Sally']}/>,
    document.getElementById("root6")
)

    ////////////////////////
    var element = <input className="nameInput"/>
ReactDOM.render(
    element,
    document.getElementById("root7")
)

    ////////////////////////
    var element = <input style={{backgroundColor: 'blue', height: 50}} />;
ReactDOM.render(
    element,
    document.getElementById("root8")
);

    ////////////////////////
    var num = 0;
    var element = <div> {num} </div>
    ReactDOM.render(
        element,
        document.getElementById("root9")
    )
    num++;
    ReactDOM.render(
        element,
        document.getElementById("root9")
    )
    num++;
