import { Button } from "./components/Button"
import { Input } from "./components/Input"

import TaxiLogo from "../public/taxi-logo.jpg"

function Login() {

    const login_user = () => {
        console.log("logged in.")
    }

    return (
        <div className="grid gap-4 w-1/2 m-auto max-w-100">
            <h2 className="text-white text-xl">Log in</h2>
            <img src={TaxiLogo} className="w-40 h-40 m-auto" />
            <Input type="text" placeholder="username" />
            <Input type="password" placeholder="password" />
            <div className="w-fit justify-self-end">
                <Button text="login" onClick={login_user} />
            </div>
            <p className="hover:underline cursor-pointer
                            justify-self-start"
            >create new account</p>
        </div>
    )
}

export default Login
