import LeftSection from "./LeftSection";
import RightSection from "./RightSection";

function Hero() {
  return (
    <section className="container py-5">
      <div className="row align-items-center gy-5">
        {/* Left Content */}
        <div className="col-12 col-md-6">
          <LeftSection />
        </div>

        {/* Right Image */}
        <div className="col-12 col-md-6">
          <RightSection />
        </div>
      </div>
    </section>
  );
}

export default Hero;
