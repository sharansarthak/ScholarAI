import { Form, Button, FloatingLabel, Container, Row, Col } from "react-bootstrap";
import Axios from "axios";
import  googlelogo from "../assets/googleicon.png";
import  applelogo  from "../assets/appleicon.png";
import { styles } from "../styles"
import { Link } from 'react-router-dom';
import { useState } from "react";

export default function LoginPage() {
  const [usernameValidity, setUsernameValidity] = useState(false);
  function login(e) {
    e.preventDefault(); // Prevent the default form submission behavior

    Axios.post("http://127.0.0.1:5000/login", {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    })
      .then((res) => {
        const response = res.data;

        if (response.success !== undefined) {
          if (response.success) {
            localStorage.setItem("token", response.token);
            window.location.href = "http://localhost:3000/tracking";
            console.log("Login successful");
          } else {
            console.error("Login failed:", response.error);
            // Handle login failure
          }
        } else if (response.error !== undefined) {
          console.error("Login failed:", response.error);
          // Handle login failure
        } else {
          console.error("Unexpected response format:", response);
        }
      })
      .catch((error) => {
        console.error("Error during login:", error);
        // Handle other errors (e.g., network issues) here
      });
  }

  function keyPress(e) {
    if (e.key === "Enter") {
      login(e);
    }
  }

  return (
    <div style={{ minHeight: `73.3vh` }}>
      <Container style={{ maxWidth: `900px`, paddingTop: `4%`, paddingBottom: '6%' }}>
        <h2 className={`${styles.heroHeadText}`} style={{ fontWeight: 'bold', fontSize: '50px', textAlign: 'center', marginBottom: '35px' }}>Login</h2>
        <Form onSubmit={login} className="custom-signup-panel mx-auto" style={{ maxWidth: `700px` }}>
          <Row className="mb-1">
            <Col>
              <strong>Username</strong>
            </Col>
          </Row>
          <Row className="mb-3">
            <Col>
              <FloatingLabel controlId="floatingUsername" label="Username" className="mb-1">
                <Form.Control
                  id="username"
                  type="text"
                  placeholder="username"
                  // isInvalid={usernameValidity}
                  style={{ borderRadius: '10px' }}
                />
              </FloatingLabel>
            </Col>
          </Row>
          <Row className="mb-1">
            <Col>
              <strong>Password</strong>
            </Col>
          </Row>
          <Row className="mb-4">
            <Col>
              <FloatingLabel controlId="floatingPassword" label="Password" className="mb-1">
                <Form.Control
                  id="password"
                  onKeyPress={keyPress}
                  type="password"
                  placeholder="password"
                  style={{ borderRadius: '10px' }}
                />
              </FloatingLabel>
            </Col>
          </Row>
          <Row>
            <Col className="mb-3">
              <Button
                size="lg"
                className="LoginButton"
                type="submit"
                onClick={login}
                style={{ width: '100%', borderRadius: '10px', fontFamily: 'Inter', fontWeight: 'bold' }}
              >
                Login
              </Button>
            </Col>
          </Row>
          <Row className="mb-2">
            <Col className="mb-1">
              <p className="text-center">
                Don't have an account? <Link to="/signup" style={{ color: 'blue', fontWeight: 'bold' }}>Sign up</Link>
              </p>
              <Row className="mb-2" style={{ marginTop: '50px' }}>
                <Col>
                  <div className="line-div"></div>
                </Col>
                <Col>
                  <p className="text-center" style={{ color: '#808080' }}>Or sign up with</p>
                </Col>
                <Col>
                  <div className="line-div"></div>
                </Col>
              </Row>
            </Col>
          </Row>
          <Row>
            <Col>
              <Button size="lg" className="GoogleButton" href="/employersignup" style={{ borderRadius: '10px' }}>
                <img src={googlelogo} alt="Google Logo" className="google-logo" style={{ height: '35px', width: '35px' }} />
              </Button>
            </Col>
            <Col>
              <Button size="lg" className="GoogleButton" href="/anotherlink" style={{ borderRadius: '10px' }}>
                <img src={applelogo} alt="Apple Image" className="apple-logo" style={{ height: '35px', width: '33px' }} />
              </Button>
            </Col>
            <Col>
              <Button size="lg" className="GoogleButton" href="/anotherlink" style={{ borderRadius: '10px' }}>
                <img src={applelogo} alt="Apple Image" className="apple-logo" style={{ height: '35px', width: '33px' }} />
              </Button>
            </Col>
          </Row>
        </Form>
        <p className={`${styles.sectionHeadText}`} style={{ fontSize: '20px', textAlign: 'center', marginTop: '25px' }}>GPT-powered AI scholarship application tool!</p>
      </Container>
    </div>
  );
}
