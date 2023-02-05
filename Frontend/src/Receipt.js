import { useEffect, useState } from "react";
import { useParams } from "react-router";
import './Receipt.css'
import YouTube from 'react-youtube'
import AwesomeSlider from 'react-awesome-slider';
import 'react-awesome-slider/dist/styles.css';
import 'react-awesome-slider/dist/custom-animations/cube-animation.css';


const RECEIPT_DETAILS_URL = "http://localhost:8080/api/v1/receipt-details/";
const THUMB_URL = "http://localhost:8080/";

function Receipt() {
    let { receipt } = useParams();
    const [data, setData] = useState({});
    useEffect(() => {
        const fetchReceipt = async () => {
            const response = await (
                    await fetch(RECEIPT_DETAILS_URL + receipt)
                ).json();
                setData(response.receipt);
            };
            fetchReceipt();
    }, []);

    return (
        <div className="container-fluid" style={
            {
                paddingLeft: "7%",
                paddingRight: "7%"
            }
        }>
            <h1>{data.name}</h1>
            <div className="row">
                <div className="col-lg">
                    <img width="50%" src={THUMB_URL + data.thumbnail} style={{
                        borderRadius: "10%"
                    }} />
                    <p className="receipt-source">Source: <a href={data.source}>{data.source}</a></p>
                    {data.youtube_link ? <div style={{
                        paddingTop: "20px"
                    }}>
                        <YouTube videoId={data.youtube_link.split("=")[1]}/>                    
                    </div> : ""}
                </div>
                <div className="col-lg">
                    <div className="row">
                        <div className="col-sm params">Category: {data.category}</div>
                        <div className="col-sm params">Area: {data.area}</div>
                        <div className="col-sm params">Tags: {data.tags ? 
                            data.tags.map(tag => {return tag.name + " "; } )
                        : ""}</div>
                        <div className="col-sm params">Date added: </div>
                    </div>
                    <h2 style={{
                        paddingTop: "30px"
                    }}>Receipt: </h2>
                    <p>{data.instructions}</p>
                    <hr />
                    <h2 style={{
                        paddingTop: "30px"
                    }}>Ingridients: </h2>
                   
                   <div className="row" style={
                            {
                                paddingTop: "10px",
                                paddingBottom: "10px"
                            }
                        }> 
                            <div className="col-sm"></div>
                            <div className="col-sm">have</div>
                            <div className="col-sm">need</div>
                    </div>
                    {data.products ? data.products.map((product, index) => {
                        return (
                        <div key={index} className="row" style={
                            {
                                paddingTop: "10px"
                            }
                        }> 
                            <div className="col-sm devider">{product.name}</div>
                            <div className="col-sm">0</div>
                            <div className="col-sm">{product.amount} {product.unit}</div>
                        </div>);
                    }) : ""}
                    <div className="d-flex justify-content-center" style={{
                        width: "30%",
                        paddingTop: "30px"
                    }}>
                        <AwesomeSlider>
                            {
                                data.products ? data.products.map((product, index)=> {
                                    return(
                                        <div key={index} data-src={THUMB_URL + product.thumbnail} />
                                    );
                                }) : ""
                            }
                        </AwesomeSlider>
                    </div> 
                </div>
            </div>

        </div>
    );
}

export default Receipt;