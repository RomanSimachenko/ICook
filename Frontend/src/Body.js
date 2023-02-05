import React from "react";
import './Body.css'
import {Col, Row} from "react-bootstrap";
import FilterBox from "./FilterBox";
import Container from 'react-bootstrap/Container';
import {CSSTransition} from 'react-transition-group'

const API_URL = "http://localhost:8080/api/v1/receipts/";

class Body extends React.Component {
    constructor() {
        super();
        this.loadMore = this.loadMore.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.prevPage = this.prevPage.bind(this);
        this.state = {
            page: 1,
            page_size: 12,
            receipts: [],
            total: 0,
            filter: '',
            search_query: '',
            isLoading: true
        }
    }

    componentDidMount() {
        this.fetchReceipts();
    }

    loadMore() {
        this.setState(prev_size => ({
            page_size: prev_size.page_size + 12,
            isLoading: true
        }), this.fetchReceipts)      
    }

    nextPage() {
        this.setState(prev_page => ({
            page: prev_page.page + 1,
            page_size: 12,
            isLoading: true
        }), this.fetchReceipts);
    }

    prevPage() {
        this.setState(prev_page => ({
            page: prev_page.page == 1 ? 1 : prev_page.page - 1,
            page_size: 12,
            isLoading: true
        }), this.fetchReceipts);
    }

    fetchReceipts() {
        console.log(API_URL + this.state.filter + `search=${this.state.search_query};page=${this.state.page};page_size=${this.state.page_size}`);
        fetch(API_URL + this.state.filter + `search=${this.state.search_query};page=${this.state.page};page_size=${this.state.page_size}`)
        .then(res => res.json())
        .then(data => {
            this.setState({
                receipts: data['receipts'],
                total: data.total,
                isLoading: false
            });
        })
        .catch(err => {
            console.error(err);
        })
    }

    applyFilters(filter_s) {
        this.setState({
            page: 1,
            page_size: 12,
            filter: filter_s,
            isLoading: true
        }, this.fetchReceipts);
    }

    applySearchQuery(query) {
        this.setState({
            page: 1,
            page_size: 12,
            search_query: query,
            isLoading: true
        }, this.fetchReceipts);
    }

    render() {
        return (
            <div className="py-5 container-bg">
                <Container className="d-flex justify-content-start">
                    <Row>
                        <Col md={3} >
                            <Row className="filter-box-container">
                            <FilterBox show_filters={true} body={this} />
                            </Row>
                        </Col>
                        <Col md={9}>
                            <div className="receipt-count-container">
                                <span className="text-count">Receipts Shown </span>
                                <span className="receipt-count">{this.state.total}</span>
                            </div>
                            <CSSTransition
                            in={this.state.isLoading}
                            timeout={1000}
                            classNames="my-node">
                            <div className="row gx-2 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
                                {this.state.receipts.map(receipt => {
                                    let stars = [];
                                    for (let i = 0; i < receipt.cooking_difficulty; i++) {
                                        stars.push(<div className="bi-star-fill"></div>);
                                    }
                                    let image_url = `http://localhost:8080/${receipt.thumbnail}`;
                                    return (
                                    <div key={receipt.id} className="col mb-3 receipt-card">
                                            <div className="card h-100">
                                                <img className="card-img-top" src={image_url} alt="..." />
                                                <div className="card-body p-1">
                                                    <div className="text-center">
                                                        <h5 className="fw-bolder" style={{
                                                            color: "black"
                                                        }}>{receipt.name}</h5>
                                                        <div className="d-flex justify-content-center small text-warning mb-2">
                                                            {stars.map(star => star)}
                                                        </div>
                                                        <span>Category: {receipt.category}</span>
                                                        <br />
                                                        <span>Area: {receipt.area}</span>
                                                    </div>
                                                </div>
                                                <div className="card-footer pt-0 border-top-0 bg-transparent">
                                                    <div className="text-center">
                                                        <a className="btn btn-outline-dark mt-auto" href={"/receipt/" + receipt.slug}>See the receipt</a>
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
                            <a className="btn btn-outline-dark mt-auto" href="#">More receipts</a>
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
            </div>
        );
    }
}

export default Body;