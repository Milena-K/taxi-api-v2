import { Button } from "./components/Button"
import { Input } from "./components/Input"

import TaxiLogo from "../public/taxi-logo.jpg"

function Login() {

    const login_user = () => {
        console.log("logged in.")
    }

    return (
        <div className="flex m-auto h-full max-w-6xl">
            <div className="invisible h-0 w-0 grow-0 flex
                            md:grow md:visible md:h-full md:w-full lg:visible">
                <img src={TaxiLogo} className="w-1/2
                                    max-w-90 max-h-90 m-auto self-center" />
            </div>
            <div className="grow h-full flex w-full">
                <div className="grid gap-4 w-fit justify-self-center m-auto
                                md:border md:rounded-2xl md:p-9 md:align-center
                                ">
                    <h4 className="text-center mb-10 md:mb-20">Log in</h4>
                    <img src={TaxiLogo} className="w-40 h-40 m-auto md:hidden" />
                    <Input type="text" placeholder="username" />
                    <Input type="password" placeholder="password" />
                    <div className="w-fit justify-self-end">
                        <Button text="login" onClick={login_user} />
                    </div>
                    <p className="hover:underline cursor-pointer
                            justify-self-start md:mt-10"
                    >create new account</p>
                </div>
            </div>
        </div>
    )
}

export default Login
