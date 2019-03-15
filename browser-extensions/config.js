const fs = require('fs');
const { browsersSupported, name, version, description } = require('./package.json');

const config = {
    sourceDirectory: './src',
    distDirectory: './dist'
};

const generateManifest = (browser) => {
    const { specifics, ...manifest } = require('./manifest.json');

    const browserSpecificManifest = specifics[browser] || {};

    const manifestToSave = {
        name,
        version,
        description,
        ...manifest,
        ...browserSpecificManifest,
    };

    fs.writeFileSync(`${config.distDirectory}/${browser}/manifest.json`, JSON.stringify(manifestToSave));
};

const generateManifests = () => browsersSupported.forEach((browser) => generateManifest(browser));

const injectOSIntoBrowserExtension = (fileName, browser) => fs
    .appendFileSync(fileName, '\n\n' + fs.readFileSync(`${config.sourceDirectory}/helpers/${browser}.js`));


const generateDistFolder = () => {
    const dirListToGenerate = [config.distDirectory];


    browsersSupported.forEach((browser) => {
        dirListToGenerate.push(`${config.distDirectory}/${browser}`);
        dirListToGenerate.push(`${config.distDirectory}/${browser}/src`);
    });

    dirListToGenerate.forEach((dir) => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }
    })
};


const filesToWorkWith = fs
    .readdirSync(config.sourceDirectory, { withFileTypes: true })
    .filter(file => file.includes('.'));

const copyFiles = () => {
    browsersSupported.forEach((browser) => {
       const browserDestDir = `${config.distDirectory}/${browser}/src`;

        filesToWorkWith.forEach((fileName) => {
            const sourceFile = `${config.sourceDirectory}/${fileName}`;
            const destinationFile = `${browserDestDir}/${fileName}`;

            console.log(`Copying ${sourceFile} to ${destinationFile}...`);

            fs.copyFileSync(sourceFile, destinationFile);

            if (fileName.includes('index.js')) {
                injectOSIntoBrowserExtension(destinationFile, browser);
            }
        });
    });
};

const watchFiles = () => {
    fs.watch(config.sourceDirectory, (event, fileName) => {
        if (!fileName.includes('__jb_old__')) {
            console.log(`File: ${fileName} has changed!`);
            copyFiles();
        }
    });

    fs.watchFile(`./manifest.json`, () => {
        console.log('File: Manifest has changed');

        generateManifests();
    })
};

generateDistFolder();
copyFiles();
generateManifests();

if (process.argv.includes('--watch')) {
    watchFiles();
}