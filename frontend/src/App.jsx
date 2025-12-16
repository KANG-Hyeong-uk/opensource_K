import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Analysis from './pages/Analysis';
import ApiDocs from './pages/ApiDocs';
import ApiUsage from './pages/ApiUsage';
import AiEvalDocs from './pages/AiEvalDocs';  // Imported
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/ai-eval" element={<AiEvalDocs />} /> { /* Added Route */}
          <Route path="/api-usage" element={<ApiUsage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          {/* Note: API Docs in GNB was requested, but I listed it as "API Reference" in previous steps? 
              Wait, user requested "API 사용량" in GNB.
              But user also asked for "API 사용법" page link.
              Wait, GNB items: Home, 분석, API 사용량, 로그인/회원가입.
              Where does "API 사용법" go? Maybe inside "API 사용량" or a separate link?
              Re-reading request: "분석 페이지에는 산출물 6개... API사용법은 ... 그리고 API 사용량은..."
              "상단바는 home, 분석, API 사용량, 로그인/회원가입이야"
              
              Hmm, so "API 사용법" is requested but not in GNB? 
              I should probably add a link to it from Footer or maybe Home features?
              Or maybe I messed up the GNB request.
              Let's put it as a route "/docs" and maybe link it from Home or Footer.
              For now, I'll make it accessible via "/docs" route.
          */}
          <Route path="/docs" element={<ApiDocs />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
