import React from "react";
import './Body.css'
import {Col, Row} from "react-bootstrap";
import FilterBox from "./FilterBox";
import Container from 'react-bootstrap/Container';
import {CSSTransition} from 'react-transition-group'
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const API_URL = "http://localhost:8080/api/v1/products/";

class ProductsBody extends React.Component {
    constructor() {
        super();
        this.loadMore = this.loadMore.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.prevPage = this.prevPage.bind(this);
        this.addToCart = this.addToCart.bind(this);
        this.closeSuccess = this.closeSuccess.bind(this);
        this.state = {
            page: 1,
            page_size: 12,
            products: [],
            total: 0,
            search_query: '',
            isLoading: true,
            success_message: false,
            lastProduct: ''
        }
    }

    componentDidMount() {
        this.fetchProducts();
    }

    loadMore() {
        this.setState(prev_size => ({
            page_size: prev_size.page_size + 12,
            isLoading: true
        }), this.fetchProducts)      
    }

    nextPage() {
        this.setState(prev_page => ({
            page: prev_page.page + 1,
            page_size: 12,
            isLoading: true
        }), this.fetchProducts);
    }

    prevPage() {
        this.setState(prev_page => ({
            page: prev_page.page == 1 ? 1 : prev_page.page - 1,
            page_size: 12,
            isLoading: true
        }), this.fetchProducts);
    }

    fetchProducts() {
        fetch(API_URL + `search=${this.state.search_query};page=${this.state.page};page_size=${this.state.page_size}`)
        .then(res => res.json())
        .then(data => {
            this.setState({
                products: data['products'],
                total: data.total,
                isLoading: false
            });
        })
        .catch(err => {
            console.error(err);
        })
    }

    applySearchQuery(query) {
        this.setState({
            page: 1,
            page_size: 12,
            search_query: query,
            isLoading: true
        }, this.fetchProducts);
    }

    closeSuccess() {
        this.setState({
            success_message: false
        })
    }

    addToCart(event) {
        console.log(event.target.id);
        this.setState({
            success_message: true,
            lastProduct: event.target.id
        });
        if (sessionStorage.getItem("products") == null) {
            let products = []
            products.push({
                    name: event.target.id,
                    slug: event.target.name,
                    count: 1
                }
            );
            sessionStorage.setItem("products", JSON.stringify(Array.from(products)));
            sessionStorage.setItem("products_count", products.size);
        } else {
            let products = JSON.parse(sessionStorage.getItem("products"));
            if (products.filter(product => product.slug == event.target.name).length == 0) {
                products.push({
                    name: event.target.id,
                    slug: event.target.name,
                    count: 1
                });
            } else {
                products = products.filter(product => {
                    if (product.slug == event.target.name) product.count += 1;
                    return product
                });
            }
            sessionStorage.setItem("products", JSON.stringify(Array.from(products)));
            sessionStorage.setItem("products_count", products.size);
        }
        console.log(sessionStorage.getItem("products"));
    }

    render() {
        return (
            <div className="py-5 container-bg">
                <Container className="d-flex justify-content-start">
                    <Row>
                        <Col md={2} >
                            <Row className="filter-box-container">
                            <FilterBox show_filters={false} body={this} />
                            </Row>
                        </Col>
                        <Col md={10}>
                            <div className="receipt-count-container">
                                <span className="text-count">Products Shown </span>
                                <span className="receipt-count">{this.state.total}</span>
                            </div>
                            <CSSTransition
                            in={this.state.isLoading}
                            timeout={1000}
                            classNames="my-node">
                            <div className="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
                                {this.state.products.map(product => {
                                    let image_url = `http://localhost:8080/${product.thumbnail}`;
                                    return (
                                    <div key={product.id} className="col mb-5 receipt-card">
                                            <div className="card h-100">
                                                <img className="card-img-top" src={image_url} alt="..." />
                                                <div className="card-body p-4">
                                                    <div className="text-center">
                                                        <h5 style={
                                                            {
                                                                color: "black"
                                                            }
                                                        } className="fw-bolder">{product.name}</h5>
                                                    </div>
                                                </div>
                                                <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                                    <div className="text-center">
                                                        <input id={product.name} onClick={this.addToCart} name={product.slug} type="button" value={"Add to cart"} className="btn btn-outline-dark mt-auto" />
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="spinner-container">
                                                <div className="loading-spinner"></div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                            </CSSTransition>

                        </Col>
                    </Row>
                </Container>
                <div onClick={this.loadMore} className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                        <div className="text-center">
                            <a className="btn btn-outline-dark mt-auto" href="#">More products</a>
                        </div>
                </div>
                <nav aria-label="Page navigation example">
                    <ul className="pagination justify-content-center">
                        <li className="page-item">
                        <a onClick={this.prevPage} className="page-link" href="#" tabIndex={-1}>Previous</a>
                        </li>
                        <li className="page-item">
                        <a onClick={this.nextPage} className="page-link" href="#">Next</a>
                        </li>
                    </ul>
                </nav>
                <Snackbar
                    anchorOrigin={{"vertical": "top", "horizontal": "center"}}
                    open={this.state.success_message}
                    onClose={this.closeSuccess}
                    severity="success"
                    key={this.state.vertical + this.state.horizontal}
                    autoHideDuration={1000}
                >
                    <MuiAlert onClose={this.closeSuccess} severity="success">
                        {`Successfully added ${this.state.lastProduct} to cart`}
                    </MuiAlert>
                </Snackbar>
            </div>
        );
    }
}

export default ProductsBody;