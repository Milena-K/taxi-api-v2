import { BrowserRouter, Route, Routes } from "react-router"
import Login from "./Login"
import App from "./App"


function RouteConfig() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </BrowserRouter>
    )
}

export default RouteConfig
