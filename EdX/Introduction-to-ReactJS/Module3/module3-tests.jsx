/**
 * React render HTML function
 */
ReactDOM.render
(
  <div>
    <HelloWorld/>
    <hr/>
    
    <ArrayElementsLoop/>
    <hr/>

    <ArrayElementsMap/>
    <hr/>

    <ArrayElementsMap2/>
    <hr/>

    <RenderArrayElementsMap3/>
    <hr/>

    <RenderArrayElementsMap3/>
    <ht/>

    <RenderArrayElementsId4/>
    <ht/>

    <Empty n="1"/>
    <hr/>
  </div>,
	document.getElementById("root")
)

/**
 * HelloWorld
 */
function HelloWorld()
{
    return(
        <h2>Hello World</h2>
    );
}

/**
 * Empty project
 */
function Empty(props)
{
    return(
        <h2>Ex {props.n}</h2>
    );
}

/**
 * Function component wich renders a list of elements using a for loop and a list.
 */
function ArrayElementsLoop(props)
{
    let elements = [];
    let array = [1, 2, 3, 4, 5];
    for (let i = 0; i < array.length; i++)
    {
        console.log("-- array[" + i + "] = " + array[i])
        elements.push(<li>{array[i]}</li>)
    }
    return (
        <ol>{elements}</ol>
    );

}

/**
 * Function component wich renders a list of elements using map.
 */
function ArrayElementsMap(props)
{
  // a giver map of elements
  let array = [
    {product:"Apple", price:3},
    {product:"Banana", price:1},
    {product:"Carrot", price:2},
    {product:"Donuts", price:5},
    {product:"Eggplant", price:4}
  ]

  // now map the elements
  let elements = array.map(
    (item) => {
        return(
          <li>Product: {item.product}, Price: ${item.price}</li>
        );
    }
  );
  
  return(
    <div>
      <h2>ArrayElementsMap1</h2>
      <ul>{elements}</ul>
    </div>
  );
}

function ArrayElementsMap2(props)
{
  let array = [
    {product:"Apple", price:3},
    {product:"Banana", price:1},
    {product:"Carrot", price:2},
    {product:"Donuts", price:5},
    {product:"Eggplant", price:4}
  ]
  return(
    <div>
      <h2>ArrayElementsMap2</h2>
        <ol>
          {
            array.map(
              (item) => {
                return(
                  <li>
                    Product: {item.product}, Price: ${item.price}
                  </li>
                );
              }
            )
          }
        </ol>      
    </div>
  );
}

function ArrayElementsMap3(props)
{
  console.log("-- ArrayElementsMap3");
  console.log(props.array.length);
  return(
    <ol>
      {
        props.array.map(
          (item) => {
            return(
              <li>
                Product:{item.product} | Price {item.price}
              </li>
            );
          }
        )
      }
    </ol>
  );  
}

function RenderArrayElementsMap3(props)
{
  let theMapArray = [
    {product:"MAÇA", price:3},
    {product:"BANANA", price:1},
    {product:"CENOURA", price:2},
    {product:"SONHO", price:5},
    {product:"BERINGELA", price:4},
    {product:"ABACATE", price:6}
  ];
  return(
    <div>
      <h2>RenderArrayElementsMap3</h2>
      <ArrayElementsMap3 array={theMapArray} />
    </div>
  );
}



function ArrayElementsId4(props)
{
  console.log("-- ArrayElementsMap3");
  console.log(props.array.length);
  return(
    <ol>
      {
        props.array.map(
          (item) => {
            return(
              <li key={item.id}>
                Product:{item.product} | Price {item.price}
              </li>
            );
          }
        )
      }
    </ol>
  );  
}

function RenderArrayElementsId4(props)
{

    let prods = [
      {id:1, product:"abacate", price:2},
      {id:2, product:"banana", price:4},
      {id:3, product:"carambola", price:6},
      {id:4, product:"damasco", price:8},
      {id:5, product:"espinafre", price:10},
      {id:6, product:"framboesa", price:12}
    ];

  return(
    <div>
      <h2>RenderArrayElementsId4</h2>
      <ArrayElementsId4 array={prods} />
    </div>  
  );
}




