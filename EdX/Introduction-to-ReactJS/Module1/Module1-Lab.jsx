
function Module1Module1Header(props)
{
    let element =
    <div>
        <h1>Welcome to React Transportation</h1>
        The best place to buy vehicles online
    </div>;
    return element;
}

function Options(props)
{
    let element =
    <div>
        <h2>Choose Options</h2>
        New Only
        <input type="checkbox" id="coding" name="interest" value="coding" checked={props.checked}/>
        <p/> Select Type
        <select>
            <option value ="All">All</option>
            <option value ="Cars">Cars</option>
            <option value ="Trucks">Trucks</option>
            <option value ="Convertibles">Convertibles</option>
        </select>
    </div>;
    return element;
}

function ProdList(props)
{
    let prodList = [];
    for (let i=0; i<props.products.length; i++)
    {
        prodList.push(<Product year={props.products[i][0]} model={props.products[i][1]} price={props.products[i][2]} />);
    }
    return <div><h2>{props.title}</h2> {prodList} </div>;
}
function Price (props)
{
    let element =
    <div> $ {props.price},00</div>;
    return element;
}
function BuyButton (props)
{
    let element =
    <div>
    <button> Buy </button>
    </div>;
    return element;
}
function Product (props){
    let element =
        <div>
            <table >
                <tr >
                    <th>Year</th>
                    <th>Model</th>
                    <th>Price</th>
                    <th>Buy</th>
                </tr>
                <tr>
                    <th>{props.year}</th>
                    <th>{props.model}</th>
                    <th> <Price price={props.price}/> </th>
                    <th> <BuyButton/> </th>
                </tr>
            </table>
        </div>
    return element;
}


// Build Module 1 App
function Module1LabApp()
{
    let element =
    <div>
        <Module1Module1Header/>
        <Options checked={false}/>
        <ProdList title="Cars List"
            products={[[2013, 'A', 32000],
                                [2011, 'B', 4400],
                                [2016, 'B', 15500]]}/>
        <ProdList title="Trucks List"
            products={[[2014, 'D', 18000],
                                [2013, 'E', 5200]]}/>
        <ProdList title="Convertibles List"
            products={[[2009, 'A', 2000],
                                [2010, 'G', 6000],
                                [2012, 'H', 12500],
                                [2017, 'M', 50000]]}/>
    </div>;
    return element;
}
ReactDOM.render(
    <Module1LabApp/>,
    document.getElementById("root")
)