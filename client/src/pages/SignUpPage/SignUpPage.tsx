import SignUpForm from "../../components/SignUpForm/SignUpForm.tsx";
import Layout from "../../components/Layout/Layout.tsx";

export default function SignUpPage() {
  return (
    <Layout>
      <div className="px-10 md:px-20 py-[7rem] font-geist-light">
        <div className="mb-15">
          <h1 className="font-geist-light font-bold text-2xl">Get started</h1>
          <p>Create a new account</p>
        </div>

        <SignUpForm />
      </div>
    </Layout>
  );
}
