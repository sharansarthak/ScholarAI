import {
  Form,
  Button,
  FloatingLabel,
  Container,
  Row,
  Col,
} from "react-bootstrap";
  import { useState } from "react";
import { styles } from "../styles"
import Axios from "axios";
import  googlelogo from "../assets/googleicon.png";
import  applelogo  from "../assets/appleicon.png";
import { Link } from 'react-router-dom';

export default function SignupPage() {
  const [emailValidity, setEmailValidity] = useState(false);
  const [firstNameValidity, setFirstNameValidity] = useState(false);
  const [lastNameValidity, setLastNameValidity] = useState(false);
  const [phoneValidity, setPhoneValidity] = useState(false);
  const [usernameValidity, setUsernameValidity] = useState(false);
  const [passwordValidity, setPasswordValidity] = useState(false);
  const [confirmPasswordValidity, setConfirmPasswordValidity] = useState(false);

  function signup() {
    if (validateFields()) {
      Axios.post("http://127.0.0.1:5000/api/signup", {
        email: document.getElementById("email").value,
        firstName: document.getElementById("firstName").value,
        lastName: document.getElementById("lastName").value,
        phoneNumber: document.getElementById("phone").value,
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
      }, {
        headers: {'Access-Control-Allow-Origin': '*'},
      })
        .then((res) => {
          localStorage.setItem("token", res.data.token);
          window.location.href = "http://localhost:3000/tracking";
        })
        .catch((res) => {
          console.log(res);
        });
    }
  }

  function validateFields() {
    let returnVal = true;
    if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(document.getElementById("email").value)
    ) {
      returnVal = false;
      setEmailValidity(true);
    }
    if (document.getElementById("firstName").value.length < 2) {
      returnVal = false;
      setFirstNameValidity(true);
    }
    if (document.getElementById("lastName").value.length < 2) {
      returnVal = false;
      setLastNameValidity(true);
    }
    if (
      !/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im.test(
        document.getElementById("phone").value
      )
    ) {
      returnVal = false;
      setPhoneValidity(true);
    }
    if (document.getElementById("username").value.length < 3) {
      returnVal = false;
      setUsernameValidity(true);
    }
    if (
      document.getElementById("password").value !==
      document.getElementById("confirmPassword").value
    ) {
      console.log("test")
      returnVal = false;
      setConfirmPasswordValidity(true);
    }
    if (document.getElementById("password").value.length < 6) {
      returnVal = false;
      setPasswordValidity(true);
    }
    return returnVal;
  }

  return (
    <div style={{ minHeight: `73.3vh` }}>
      <Container style={{ maxWidth: `900px`, paddingTop: `4%`, paddingBottom:'6%'}}>
      <h2 className={`${styles.heroHeadText}`} style={{ fontWeight: 'bold', fontSize: '50px', textAlign: 'center' }}>Ready to apply for scholarships?</h2>
      <p className={`${styles.sectionHeadText}`} style={{ fontSize: '20px', textAlign: 'center', marginBottom: '25px' }}>Quickly register and find the perfect scholarship for you!</p>
      <Form className="custom-signup-panel mx-auto" style={{ maxWidth: `700px` }} noValidate>
        <Row className="mb-1">
          <Col>
            <strong>First Name</strong>
          </Col>
          <Col>
            <strong>Last Name</strong>
          </Col>
        </Row>
        <Row className="mb-3">
          <Col>
            <FloatingLabel controlId="floatingFirstName" label="First Name" className="mb-1">
              <Form.Control
                id="firstName"
                type="text"
                placeholder="First Name"
                isInvalid={firstNameValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
          <Col>
            <FloatingLabel controlId="floatingLastName" label="Last Name" className="mb-1">
              <Form.Control
                id="lastName"
                type="text"
                placeholder="Last Name"
                isInvalid={lastNameValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
        </Row>
        <Row className="mb-1">
          <Col>
            <strong>Email Address</strong>
          </Col>
        </Row>
        <Row className="mb-3">
          <Col>
            <FloatingLabel controlId="floatingEmail" label="Email address" className="mb-1">
              <Form.Control
                id="email"
                type="email"
                placeholder="name@sweseek.com"
                required
                isInvalid={emailValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
        </Row>
        <Row className="mb-1">
          <Col>
            <strong>Phone Number</strong>
          </Col>
        </Row>
        <Row className="mb-3">
          <Col>
            <FloatingLabel controlId="floatingPhone" label="Phone Number" className="mb-1">
              <Form.Control
                id="phone"
                type="tel"
                placeholder="444-444-4444"
                pattern="[0-9]{3} [0-9]{3} [0-9]{4}"
                maxLength="12"
                isInvalid={phoneValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
        </Row>
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
                isInvalid={usernameValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
        </Row>
        <Row className="mb-1">
          <Col>
            <strong>Password</strong>
          </Col>
          <Col>
            <strong>Confirm Password</strong>
          </Col>
        </Row>
        <Row className="mb-3">
          <Col>
            <FloatingLabel controlId="floatingPassword" label="Password" className="mb-1">
              <Form.Control
                id="password"
                type="password"
                placeholder="password"
                isInvalid={passwordValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
          <Col className="mb-4">
            <FloatingLabel controlId="floatingConfirmPassword" label="Confirm Password" className="mb-1">
              <Form.Control
                id="confirmPassword"
                type="password"
                placeholder="password"
                isInvalid={confirmPasswordValidity}
                style={{ borderRadius: '10px' }}
              />
            </FloatingLabel>
          </Col>
        </Row>
        <Row className="mb-0">
            <Col className="mb-2">
              <Button size="lg" className="SignupLoginButton" onClick={signup} style={{ width: '100%', borderRadius: '10px', fontFamily: 'Inter', fontWeight:'bold' }}>
                Register
              </Button>
            </Col>
          </Row>
          <Row className="mb-2">
            <Col className="mb-1">
              <p className="text-center">
                Already have an account? <Link to="/login" style={{ color: 'blue', fontWeight: 'bold' }}>Log in</Link>
              </p>
              <Row className="mb-2" style={{ marginTop: '50px'}}>
              <Col>
                <div className="line-div"></div>
              </Col>
              <Col>
                <p className="text-center"  style={{ color: '#808080' }}>Or sign up with</p>
              </Col>
              <Col>
                <div className="line-div"></div>
              </Col>
              </Row>
            </Col>
          </Row>
          <Row>
            <Col>
              <Button size="lg" className="GoogleButton" href="/employersignup" style ={{borderRadius: '10px'}}>
                <img src ={ googlelogo } alt="Google Logo" className="google-logo" style={{ height: '35px', width: '35px'}} /> 
              </Button>
            </Col>
            <Col>
              <Button size="lg" className="GoogleButton" href="/anotherlink" style ={{borderRadius: '10px'}}>
                <img src={ applelogo } alt="Apple Image" className="apple-logo" style={{ height: '35px', width: '33px'}} /> 
              </Button>
            </Col>
            <Col>
              <Button size="lg" className="GoogleButton" href="/anotherlink" style ={{borderRadius: '10px'}}>
                <img src={ applelogo } alt="Apple Image" className="apple-logo" style={{ height: '35px', width: '33px'}} /> 
              </Button>
            </Col>
        </Row>
      </Form>
      <p className={`${styles.sectionHeadText}`} style={{ fontSize: '20px', textAlign: 'center', marginTop: '25px' }}>GPT-powered AI scholarship application tool!</p>
    </Container>
    </div>
  );
}
