from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
import io

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and extractor
model_name = "dima806/medicinal_plants_image_detection"
model = AutoModelForImageClassification.from_pretrained(model_name)
extractor = AutoFeatureExtractor.from_pretrained(model_name)

plant_info = {
    "Amla": {
        "benefit": "Rich in Vitamin C; boosts immunity and digestion.",
        "soil": "Well-drained loamy soil.",
        "appearance": "Bright green leaves with fine parallel veins.",
        "region": "Widely found across India, especially in tropical regions.",
    },
    "Curry": {
        "benefit": "Improves digestion and controls blood sugar levels.",
        "soil": "Moist, well-drained soils rich in organic matter.",
        "appearance": "Dark green pinnate leaves with smooth edges.",
        "region": "South India and tropical parts of the country.",
    },
    "Betel": {
        "benefit": "Used as a mouth freshener and has antimicrobial properties.",
        "soil": "Sandy loam with good drainage and organic content.",
        "appearance": "Shiny heart-shaped leaves with prominent veins.",
        "region": "Eastern and southern India.",
    },
    "Bamboo": {
        "benefit": "Used in traditional medicine for respiratory issues.",
        "soil": "Well-drained sandy loam soils.",
        "appearance": "Narrow lance-shaped leaves with parallel venation.",
        "region": "North-east India, sub-Himalayan belt.",
    },
    "Palak(Spinach)": {
        "benefit": "Rich in iron, vitamins, and antioxidants.",
        "soil": "Moist, nitrogen-rich loamy soil.",
        "appearance": "Dark green soft oval leaves with reticulate veins.",
        "region": "Cultivated across India.",
    },
    "Coriender": {
        "benefit": "Aids digestion and lowers cholesterol levels.",
        "soil": "Well-drained loamy or sandy soil.",
        "appearance": "Delicate, feathery green leaves.",
        "region": "Commonly grown in all parts of India.",
    },
    "Ashoka": {
        "benefit": "Treats gynecological disorders and pain.",
        "soil": "Sandy loam to clay loam soil.",
        "appearance": "Glossy, oblong leaves with wavy margins.",
        "region": "Western Ghats and central India.",
    },
    "Seethapala": {
        "benefit": "Boosts energy, aids digestion.",
        "soil": "Well-drained sandy or red soil.",
        "appearance": "Rounded leaves with pale green color.",
        "region": "Deccan plateau and southern states.",
    },
    "Lemon_grass": {
        "benefit": "Relieves anxiety and digestive problems.",
        "soil": "Loamy and sandy loam soils.",
        "appearance": "Long, narrow green blades with sharp margins.",
        "region": "Assam, Kerala, and Karnataka.",
    },
    "Pappaya": {
        "benefit": "Rich in enzymes aiding digestion and skin health.",
        "soil": "Light, well-drained soils rich in organic matter.",
        "appearance": "Large lobed leaves with palmate veins.",
        "region": "Tropical regions across India.",
    },
    "Curry_Leaf": {
        "benefit": "Good for eyesight, anemia, and digestion.",
        "soil": "Fertile, sandy loam soil with good drainage.",
        "appearance": "Dark green compound leaves with curved tips.",
        "region": "Common in south Indian households.",
    },
    "Lemon": {
        "benefit": "High in Vitamin C; boosts immunity.",
        "soil": "Loamy, well-drained, and slightly acidic soil.",
        "appearance": "Glossy green leaves with citrus scent.",
        "region": "Widely cultivated in central and southern India.",
    },
    "Nooni": {
        "benefit": "Boosts immunity, antibacterial properties.",
        "soil": "Dry, loamy soil with moderate moisture.",
        "appearance": "Dark green oval leaves with smooth margins.",
        "region": "Andhra Pradesh, Tamil Nadu.",
    },
    "Henna": {
        "benefit": "Used for skin, hair, and wound healing.",
        "soil": "Well-drained, sandy or loamy soils.",
        "appearance": "Pale green leaves with fine venation.",
        "region": "North-western India and Rajasthan.",
    },
    "Mango": {
        "benefit": "Lowers cholesterol, boosts memory.",
        "soil": "Well-drained, fertile alluvial soil.",
        "appearance": "Long green lance-shaped leaves with prominent midrib.",
        "region": "Pan India, especially UP, Bihar, Maharashtra.",
    },
    "Doddpathre": {
        "benefit": "Relieves cough, cold and aids digestion.",
        "soil": "Loamy soil with good moisture.",
        "appearance": "Thick green succulent leaves with rough texture.",
        "region": "South India, especially Karnataka.",
    },
    "Amruta_Balli": {
        "benefit": "Anti-inflammatory, boosts immunity.",
        "soil": "Moist, fertile soil with good drainage.",
        "appearance": "Heart-shaped leaves with fine veins.",
        "region": "Western Ghats and hilly regions.",
    },
    "Betel_Nut": {
        "benefit": "Stimulant; used in traditional medicine.",
        "soil": "Sandy loam with good drainage.",
        "appearance": "Pinnate leaves from tall areca palm.",
        "region": "Kerala, Assam, coastal Karnataka.",
    },
    "Tulsi": {
        "benefit": "Immunity booster, anti-stress herb.",
        "soil": "Rich, loamy soil with good drainage.",
        "appearance": "Fragrant green leaves with serrated edges.",
        "region": "Across India, often grown in homes.",
    },
    "Pomegranate": {
        "benefit": "Rich in antioxidants, improves heart health.",
        "soil": "Well-drained loamy or alluvial soils.",
        "appearance": "Glossy narrow leaves with smooth texture.",
        "region": "Maharashtra, Gujarat, Rajasthan.",
    },
    "Castor": {
        "benefit": "Used in pain relief and laxatives.",
        "soil": "Red loamy soil with good drainage.",
        "appearance": "Broad palmate leaves with pointed lobes.",
        "region": "Southern and central India.",
    },
    "Jackfruit": {
        "benefit": "Aids digestion and boosts energy.",
        "soil": "Sandy loam to clay soil.",
        "appearance": "Thick green oblong leaves with smooth margins.",
        "region": "Kerala, Karnataka, Tamil Nadu.",
    },
    "Insulin": {
        "benefit": "Controls blood sugar levels naturally.",
        "soil": "Well-drained fertile soil.",
        "appearance": "Broad green leaves with white midrib.",
        "region": "Southern states of India.",
    },
    "Pepper": {
        "benefit": "Improves digestion and respiratory health.",
        "soil": "Loamy soil rich in humus.",
        "appearance": "Dark green cordate leaves on climbing vines.",
        "region": "Kerala, Karnataka.",
    },
    "Raktachandini": {
        "benefit": "Purifies blood and improves skin health.",
        "soil": "Well-drained lateritic soils.",
        "appearance": "Dark green elongated leaves.",
        "region": "Western Ghats and forests of central India.",
    },
    "Aloevera": {
        "benefit": "Heals skin, improves digestion.",
        "soil": "Sandy or loamy soil with good drainage.",
        "appearance": "Fleshy, green serrated leaves with gel inside.",
        "region": "Dry regions of Rajasthan, Gujarat.",
    },
    "Jasmine": {
        "benefit": "Relieves stress, used in aromatherapy.",
        "soil": "Sandy loam with good drainage.",
        "appearance": "Small, glossy green leaves with oval shape.",
        "region": "Tamil Nadu, Karnataka.",
    },
    "Doddapatre": {
        "benefit": "Treats colds, fevers, and indigestion.",
        "soil": "Moist and well-aerated soil.",
        "appearance": "Succulent green leaves with thick texture.",
        "region": "South India.",
    },
    "Neem": {
        "benefit": "Antiseptic, antibacterial, and antifungal.",
        "soil": "Sandy, well-drained soil.",
        "appearance": "Compound pinnate green leaves with serrated edges.",
        "region": "Across India.",
    },
    "Geranium": {
        "benefit": "Used for skin ailments and aromatherapy.",
        "soil": "Loamy, well-drained soil.",
        "appearance": "Deeply lobed green leaves.",
        "region": "Himalayan regions.",
    },
    "Rose": {
        "benefit": "Soothes skin, rich in antioxidants.",
        "soil": "Loamy and well-drained with good organic matter.",
        "appearance": "Dark green compound leaves with serrated edges.",
        "region": "Pan India (cultivated).",
    },
    "Gauva": {
        "benefit": "Rich in Vitamin C, improves immunity.",
        "soil": "Alluvial to sandy loam soil.",
        "appearance": "Oval leaves with visible parallel veins.",
        "region": "North and central India.",
    },
    "Hibiscus": {
        "benefit": "Promotes hair health and reduces blood pressure.",
        "soil": "Sandy loam soil rich in organic matter.",
        "appearance": "Large green serrated leaves with a glossy finish.",
        "region": "Common in gardens across India.",
    },
    "Nithyapushpa": {
        "benefit": "Used in traditional medicine for diabetes and skin issues.",
        "soil": "Loamy or slightly acidic soils.",
        "appearance": "Glossy, oval green leaves.",
        "region": "Southern India.",
    },
    "Wood_sorel": {
        "benefit": "Anti-inflammatory and cooling herb.",
        "soil": "Humus-rich, moist soil.",
        "appearance": "Trifoliate leaves resembling clover.",
        "region": "Moist forest regions.",
    },
    "Tamarind": {
        "benefit": "Digestive aid, rich in antioxidants.",
        "soil": "Well-drained red loamy soil.",
        "appearance": "Compound pinnate leaves with many leaflets.",
        "region": "South India, Maharashtra.",
    },
    "Guava": {
        "benefit": "Boosts immunity, aids digestion.",
        "soil": "Loamy soil with good drainage.",
        "appearance": "Broad, oval leaves with symmetrical venation.",
        "region": "Cultivated all over India.",
    },
    "Bhrami": {
        "benefit": "Enhances memory and brain function.",
        "soil": "Moist, loamy soil.",
        "appearance": "Small, succulent, green rounded leaves.",
        "region": "Eastern and southern states.",
    },
    "Sapota": {
        "benefit": "Rich in iron and energy.",
        "soil": "Deep alluvial or sandy loam soil.",
        "appearance": "Oval, dark green leaves with smooth edges.",
        "region": "Maharashtra, Gujarat, Tamil Nadu.",
    },
    "Basale": {
        "benefit": "Cooling effect, rich in vitamins.",
        "soil": "Moist, loamy soil.",
        "appearance": "Thick, heart-shaped leaves.",
        "region": "Southern coastal regions.",
    },
    "Avacado": {
        "benefit": "Heart health, rich in healthy fats.",
        "soil": "Well-drained, sandy loam soil.",
        "appearance": "Large green shiny leaves with pointed tips.",
        "region": "Western Ghats and hilly areas.",
    },
    "Ashwagandha": {
        "benefit": "Reduces stress, boosts energy.",
        "soil": "Sandy loam soil with low moisture.",
        "appearance": "Dull green leaves with ovate shape.",
        "region": "Drier parts of India (MP, Rajasthan).",
    },
    "Nagadali": {
        "benefit": "Anti-inflammatory and liver health.",
        "soil": "Sandy or loamy soils.",
        "appearance": "Elongated green leaves with pointed ends.",
        "region": "Karnataka, Andhra Pradesh.",
    },
    "Arali": {
        "benefit": "Used for religious and ornamental purposes.",
        "soil": "Moist, sandy soil.",
        "appearance": "Lustrous green leaves arranged in a spiral.",
        "region": "South India.",
    },
    "Ekka": {
        "benefit": "Treats cough, asthma, and joint pain.",
        "soil": "Sandy loam soil.",
        "appearance": "Broad, dusty green leaves with rough texture.",
        "region": "Rural and semi-arid regions.",
    },
    "Ganike": {
        "benefit": "Used for anti-inflammatory and cooling purposes.",
        "soil": "Moist clay soil.",
        "appearance": "Ovate green leaves with soft hairs.",
        "region": "Southwestern India.",
    },
    "Tulasi": {
        "benefit": "Similar to Tulsi – treats cold, cough, stress.",
        "soil": "Well-drained loamy soil.",
        "appearance": "Green leaves with serrated margins and strong aroma.",
        "region": "Common across Indian households.",
    },
    "Honge": {
        "benefit": "Used in skincare and antiseptic treatments.",
        "soil": "Sandy, loamy soil.",
        "appearance": "Compound leaves with long leaflets.",
        "region": "Karnataka and Maharashtra.",
    },
    "Mint": {
        "benefit": "Aids digestion and cools the body.",
        "soil": "Rich loamy, moist soil.",
        "appearance": "Fragrant serrated leaves with green hue.",
        "region": "Pan India.",
    },
    "Catharanthus": {
        "benefit": "Used in treatment of cancer and diabetes.",
        "soil": "Well-drained loamy soil.",
        "appearance": "Oval glossy green leaves with white midrib.",
        "region": "Tamil Nadu and Kerala.",
    },
    "Papaya": {
        "benefit": "Aids digestion, skin health.",
        "soil": "Fertile, light loam with good drainage.",
        "appearance": "Palmate deeply lobed leaves.",
        "region": "All tropical regions in India.",
    },
    "Brahmi": {
        "benefit": "Improves memory, reduces anxiety.",
        "soil": "Moist and rich soil near water bodies.",
        "appearance": "Small rounded leaves with soft texture.",
        "region": "Eastern and southern India.",
    },
}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        # inputs = extractor(images=image, return_tensors="pt")

        # with torch.no_grad():
        #     outputs = model(**inputs)
        #     predicted_class_idx = outputs.logits.argmax(-1).item()
        #     label = model.config.id2label[predicted_class_idx]

        # return {"predicted_class": label}

        inputs = extractor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        class_name = model.config.id2label[predicted_class_idx]

        details = plant_info.get(class_name, {
            "benefit": "Info not available",
            "soil": "Info not available",
            "appearance": "Info not available",
            "region": "Info not available",
        })

        return {
            "prediction": class_name,
            "benefit": details["benefit"],
            "soil": details["soil"],
            "appearance": details["appearance"],
            "region": details["region"]
        }

    except Exception as e:
        return {"error": str(e)}
