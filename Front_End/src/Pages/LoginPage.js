import { Form, Button, FloatingLabel, Container, Row, Col } from "react-bootstrap";
import "../Styles/LoginAndSignupStyles.css";
import Axios from "axios";

export default function LoginPage() {
  function login() {
    Axios.get("http://127.0.0.1:5000/api/login", {
      params: {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      },
    })
      .then((res) => {
        localStorage.setItem("token", res.data.token);
        window.location.href = "http://localhost:3000/tracking";
      })
      .catch((res) => {
        console.log(res);
      });
  }

  function keyPress(e) {
    if (e.key === "Enter") {
      login();
    }
  }

  function employerLogin(){
    window.location.href = "http://localhost:3000/employerlogin";
  }

  return (
    <div style={{ minHeight: `73.3vh`, paddingTop: `8%` }}>
      <Container style={{ maxWidth: `800px` }}>
        <h1 className="SignupHeader">Login</h1>
        <Form onSubmit={login} className="SignupForm">
          <FloatingLabel
            controlId="floatingInput"
            label="Email address"
            className="mb-3"
          >
            <Form.Control
              id="email"
              type="text"
              placeholder="name@sweseek.com"
            />
          </FloatingLabel>
          <FloatingLabel
            controlId="floatingInput"
            label="Password"
            className="mb-3"
          >
            <Form.Control
              id="password"
              onKeyPress={keyPress}
              type="password"
              placeholder="password"
            />
          </FloatingLabel>
          <Row>
            <Col>
              <Button
              size="lg"
              className="SignupButton"
              type="submit"
              onClick={login}
              >
                Login
              </Button>
            </Col>
          </Row>
          <Row>
            <Col>
              <a href="http://localhost:3000/employerlogin">
                <Button
                  size="lg"
                  className="SignupButton"
                >
                  Or login as Employer
                </Button>
              </a>
            </Col>
          </Row>
        </Form>
      </Container>
    </div>
  );
}
