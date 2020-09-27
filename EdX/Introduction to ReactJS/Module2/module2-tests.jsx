// Basic Welcome class component
class Welcome extends React.Component{
    render(){
        return(
            <div>
                <h3>Message: {this.props.message}</h3>
                {this.props.testProp}
            </div>
        )
    }
}

/// this.props: are the tags passed by the the HTML tags
/// state: is the state of the class component, stored in a dictionary 
class Counter extends React.Component{
    constructor (props)
    {
        // need to initialize class props
        super(props);
        this.state = {
            foo:123,
            bar:456,
            message:"initial message",
            value:0,
            count:0};
    }
    componentDidMount(){
    //updating state
    //this.setState({message:"new message @ componentDidMount()"});
            this.setState({value:this.state.value+1});
            this.setState({value:this.state.value+1});
            this.setState({value:this.state.value+1});
            this.setState((prevState, props) => {return {message: prevState.message+'!'}});
            this.setState({count:42});
            console.log(this.state.count);
}
    render () {
        return (
            <div>
                Hello World! foo:{this.state.foo} bar:{this.state.bar}
                <br/>Message: {this.state.message}
                <br/>Value: {this.state.value}
            </div>);
    }
}

///////////////////////////////////////////////////////////////////////////////
// Event Handlers
///////////////////////////////////////////////////////////////////////////////

class Counter2 extends React.Component{
    constructor(props){
        super(props);
        this.state = {count:0}
        // binding is necessary to make this point to the correct object
        this.clickHandler = this.clickHandler.bind(this);
    }

    clickHandler(){
        // increments the count of the State
        this.setState((prevState, props)=> {
            console.log('props='+props);
            console.log('prevState.count='+prevState.count);
            return {count:prevState.count + 1}
        })
    }
    render (){
        // renders a button that displays the state count
        return <button onClick = {this.clickHandler}> {this.state.count}</button>
    }
}

///////////////////////////////////////////////////////////////////////////////
// Lifting State Up
///////////////////////////////////////////////////////////////////////////////

class Details extends React.Component{
    render(){
        return <h3>{this.props.details}</h3>
    }
}
class Button extends React.Component{
    render(){
        return (
            <button style={{color:this.props.active?'red':'blue'}} onClick={() =>
            {this.props.clickHandler(this.props.id, this.props.name)}	}>
                {this.props.name}
            </button>
        )
    }
}
class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {activeArray:[0, 0, 0, 0], details:""};
        this.clickHandler = this.clickHandler.bind(this);
    }
    clickHandler(id, details){
        let arr = [0, 0, 0, 0];
        arr[id] = 1;
        this.setState({activeArray:arr, details:details});
        console.log(id, details);
    }
    render(){
        return (
            <div>
                <Button id={0} active={this.state.activeArray[0]} clickHandler = {this.clickHandler} name="one"/>
                <Button id={1} active={this.state.activeArray[1]} clickHandler = {this.clickHandler} name="two"/>
                <Button id={2} active={this.state.activeArray[2]} clickHandler = {this.clickHandler} name="three"/>
                <Button id={3} active={this.state.activeArray[3]} clickHandler = {this.clickHandler} name="four"/>
                <Details details= {this.state.details}/>
            </div>
        )
    }
}

class Welcome2 extends React.Component{
    constructor(props){
        super(props);
        this.state = {value:123};
    }
    render(){
        return(
            <h3>Value: {this.state.value}</h3>
        );
    }
}

class Welcome3 extends React.Component{
    constructor(){
        super()
        this.state = {value:0}
                this.handleClick = this.handleClick.bind(this);
    }
    handleClick(){
      this.setState({value:this.state.value+1})
    }
    render(){
        return <button onClick = {this.handleClick}>{this.state.value}</button>
    }
}

class Counter3 extends React.Component{
    constructor(props){
        super(props)
        //initial state set up
        this.state = {message:"initial message"}
    }
    componentDidMount(){
        //updating state
        this.setState((prevState, props) => {
                        console.log("did mounnt");
            return {message: prevState.message + '!'}
        })
    }
    render(){
        return <div>Message:{this.state.message}</div>
    }
}

class Welcome4 extends React.Component{
    constructor(props){
        super(props)
        this.state = {value:0}
    }
    shouldComponentUpdate(nextProps, nextState){
        return false;
    }
    handleClick(){
      this.setState({value:this.state.value+this.props.incrementAmount})
    }
    render(){
        return <button onClick = {this.handleClick}>{this.state.value}</button>
    }
}

///////////////
class Details2 extends React.Component{
 render(){
     return <h1>{this.props.details}</h1>
 }
}
class Button2 extends React.Component{
 render(){
         return (
             <button style = {{color: this.props.active? 'red': 'blue'}} onClick={ this.clickHandler(this.props.id,this.props.name)   }>
                 {this.props.name}
             </button>
         )
 }
}
class App2 extends React.Component{
     constructor(props){
             super(props)
             this.state = {activeArray:[0,0,0,0], title:""}
             this.clickHandler = this.clickHandler.bind(this)
     }
     clickHandler(id,details){
             var arr = [0,0,0,0]
             arr[id] = 1
             this.setState({activeArray:arr,details:details})
             console.log(id,title)
     }
     render(){
             return (
                     <div>
                             <Button2 id = {0} active = {this.state.activeArray[0]} clickHandler = {this.clickHandler} name="bob"/>
                             <Button2 id = {1} active = {this.state.activeArray[1]} clickHandler = {this.clickHandler} name="joe"/>
                             <Button2 id = {2} active = {this.state.activeArray[2]} clickHandler = {this.clickHandler} name="tree"/>
                             <Button2 id = {3} active = {this.state.activeArray[3]} clickHandler = {this.clickHandler} name="four"/>
                             <Details2 details = {this.state.details}/>
                     </div>
             )
     }
}

class Counter5 extends React.Component{
 constructor(props){
     super(props)
     //initial state set up
     this.state = {count:32}
 }
 componentDidMount(){
     //updating state
     this.setState({count:42}, () => {
         console.log(this.state.count)
         this.setState({count:52})
     })
 }
 render(){
     return <div>Message:{this.state.message}</div>
 }
}

ReactDOM.render(
    <div>
        <h3> State 1</h3>
    <Welcome message="Relou Uorld!" testProp="this is a test property"/>
        <hr/>
        <h3> State 2</h3>
        <Counter/>
        <hr/>
        <h3> Event Handlers</h3>
        <Counter2/>
        <hr/>
        <h3>Lifting State Up</h3>
        <App/>
        <hr/>
        <Welcome2/>
        <hr/>
        <hr/>
        <Welcome3/>
        <hr/>
        <Counter3 />
        <hr/>
        <Welcome4 />
        <hr/>
        <Counter5 />

    </div>,
    document.getElementById("root")
)

