import Head from 'next/head';

const Layout = props => (
  <div>
    <Head>
        <title>Alfred</title>
    </Head>
    <style global jsx>{`
        body {
            /** Dynamic background, updated via API **/
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${props.background});
        }
    `}</style>
    {props.children}
  </div>
)

export default Layout
