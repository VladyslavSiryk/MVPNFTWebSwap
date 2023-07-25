const window_eth = (typeof ethereum !== 'undefined');
const delay = ms => new Promise(res => setTimeout(res, ms));
var selector_button = "#my_button",
    disable_style = "dsbl",
    network_ = "eth",
    now_address = '';
const chain_settings = {
    eth: [{
        chainId: '0x1',
        chainName: 'Ethereum',
        nativeCurrency: {
            name: 'Ethereum',
            symbol: 'ETH',
            decimals: 18,
        },
        rpcUrls: ['https://eth.llamarpc.com'],
        blockExplorerUrls: ['https://etherscan.io'],
    }],
    bsc: [{
        chainId: '0x38',
        chainName: 'Binance Smart Chain',
        nativeCurrency:
        {
            name: 'BNB',
            symbol: 'BNB',
            decimals: 18
        },
        rpcUrls: ['https://bsc-dataseed.binance.org/'],
        blockExplorerUrls: ['https://bscscan.com/'],
    }]
}

function inits() {
    if (window_eth) {
        ethereum.request({ method: 'eth_accounts' }).then(async (wallet) => {
            if (typeof(wallet[0]) != "undefined"){
                now_address = wallet[0];
                paste_address()
            }
        });
    }
}



function paste_address() {
    var formated_ad = now_address.substr(0, 4) + "..." + now_address.substr(-4);
    $('#connectButton').text('Connected ' + formated_ad).prop("disabled", true);
    var swap_username = JSON.parse(document.getElementById('userName').textContent);
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "api/web3auth",
        type: "POST",
        data: {
            wallet_address: now_address,
            public_address:formated_ad,
            current_user:swap_username,
            csrfmiddlewaretoken: csrf,
        },
        
    }); 
}


function reloadNft() {
    if (window_eth) {
        ethereum.request({ method: 'eth_accounts' }).then(async (wallet) => {
            if (typeof(wallet[0]) != "undefined"){
                now_address = wallet[0];
            }
        });
    }
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $("#collectionReload").hide();
    $("#loading-indicator").show();
    $.ajax({
        url: "api/load_tokens",
        type: "POST",
        data: {
            address: now_address,
            csrfmiddlewaretoken: csrf,
        },
        
        success: function(response){
            $("#loading-indicator").hide();
            if (response === "success"); {
                $("#loading-indicator").hide();
                $("#collectionReload").show();
                $("#collectionReload").text("Your collection successfuly  updated").prop("disabled", true);
                setTimeout(function() {
                    location.reload();
                }, 5000);
            } elif (response === "Too many requests"); {
                $("#collectionReload").show();
                $("#collectionReload").text("1 update per 10 minutes, try later").prop("disabled", true);
            }
        },
    });
};


async function getAccount() {
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    if (accounts) {
        const account = accounts[0];
        const network = await new ethers.providers.Web3Provider(window.ethereum).getNetwork().then(async (data) => {
            return data.chainId;
        });
        if (network != parseInt(chain_settings[network_][0].chainId)) {
            swith_chain()
        } else inits();
        paste_address();
    }
}
async function swith_chain() {
    try {
        await ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: (chain_settings[network_][0].chainId) }],
        }).then(async () => {
            getAccount()
        })
        return true
    } catch (switchError) {
        console.log(switchError)
        await ethereum.request({
            method: 'wallet_addEthereumChain',
            params: chain_settings[network_],
        }).then(async () => {
            swith_chain()
        })
    }
}