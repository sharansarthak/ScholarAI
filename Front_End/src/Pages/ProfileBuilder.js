import React, { useEffect } from 'react';

const ProfileBuilder = () => {
  useEffect(() => {
    const loadTypeformScript = () => {
      const script = document.createElement('script');
      script.src = "//embed.typeform.com/next/embed.js";
      script.async = true;
      document.body.appendChild(script);
    };

    loadTypeformScript();

    // Function to handle network requests
    const monitorSubmissions = () => {
      const originalFetch = window.fetch;
      window.fetch = async (...args) => {
        if (args[0].includes('complete-submission')) {
          // Redirect when the submission URL is called
          window.location.href = 'http://localhost:3000/jobs';
        }
        return originalFetch.apply(this, args);
      };
    };

    monitorSubmissions();
  }, []); 

  return (
    <div style={{ height: '100vh', width: '100vw', overflow: 'hidden' }}>
<div data-tf-live="01HFF0S2PNASCMA78W35YJQFC9"></div><script src="//embed.typeform.com/next/embed.js"></script></div>
  );
};

export default ProfileBuilder;
