import { Form, Button, FloatingLabel, Container, Row, Col } from "react-bootstrap";
import Axios from "axios";
import "../Styles/LoginAndSignupStyles.css";

export default function LoginPage() {
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
    <div style={{ minHeight: `73.3vh`, paddingTop: `8%` }}>
      <Container style={{ maxWidth: `800px` }}>
        <h1 className="SignupHeader">Login</h1>
        <Form onSubmit={login} className="SignupForm">
          <FloatingLabel controlId="floatingInput" label="Email address" className="mb-3">
            <Form.Control id="email" type="text" placeholder="name@sweseek.com" />
          </FloatingLabel>
          <FloatingLabel controlId="floatingInput" label="Password" className="mb-3">
            <Form.Control id="password" onKeyPress={keyPress} type="password" placeholder="password" />
          </FloatingLabel>
          <Row>
            <Col>
              <Button size="lg" className="SignupButton" type="submit">
                Login
              </Button>
            </Col>
          </Row>
        </Form>
      </Container>
    </div>
  );
}
