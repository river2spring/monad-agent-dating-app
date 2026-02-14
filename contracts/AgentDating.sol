// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AgentDating
 * @dev Escrow and settlement system for AI agent dating economy on Monad
 * Implements Prisoner's Dilemma payoff distribution
 */
contract AgentDating {
    
    // Payoff multipliers (scaled by 10 for precision)
    // Both cooperate: 15 (1.5x), Both defect: 5 (0.5x)
    // Defect vs Cooperate: 25 (2.5x) vs 0
    uint256 constant BOTH_COOPERATE = 15;
    uint256 constant BOTH_DEFECT = 5;
    uint256 constant DEFECTOR_WINS = 25;
    uint256 constant COOPERATOR_LOSES = 0;
    uint256 constant SCALE = 10;
    
    struct Game {
        address agent1;
        address agent2;
        uint256 stake1;
        uint256 stake2;
        bool agent1Committed;
        bool agent2Committed;
        bytes32 agent1MoveHash;
        bytes32 agent2MoveHash;
        bool agent1Revealed;
        bool agent2Revealed;
        bool agent1Cooperated;
        bool agent2Cooperated;
        bool settled;
        uint256 createdAt;
    }
    
    mapping(uint256 => Game) public games;
    uint256 public gameCounter;
    
    event GameCreated(uint256 indexed gameId, address indexed agent1, address indexed agent2, uint256 stake1, uint256 stake2);
    event MoveCommitted(uint256 indexed gameId, address indexed agent);
    event MoveRevealed(uint256 indexed gameId, address indexed agent, bool cooperated);
    event GameSettled(uint256 indexed gameId, address indexed agent1, address indexed agent2, 
                      bool agent1Cooperated, bool agent2Cooperated, uint256 payout1, uint256 payout2);
    
    /**
     * @dev Create a new game with stakes from both agents
     */
    function createGame(address agent2) external payable returns (uint256) {
        require(msg.value > 0, "Stake must be > 0");
        require(agent2 != msg.sender, "Cannot play against yourself");
        
        uint256 gameId = gameCounter++;
        
        games[gameId] = Game({
            agent1: msg.sender,
            agent2: agent2,
            stake1: msg.value,
            stake2: 0,
            agent1Committed: false,
            agent2Committed: false,
            agent1MoveHash: 0,
            agent2MoveHash: 0,
            agent1Revealed: false,
            agent2Revealed: false,
            agent1Cooperated: false,
            agent2Cooperated: false,
            settled: false,
            createdAt: block.timestamp
        });
        
        return gameId;
    }
    
    /**
     * @dev Agent 2 joins the game with their stake
     */
    function joinGame(uint256 gameId) external payable {
        Game storage game = games[gameId];
        require(msg.sender == game.agent2, "Not agent2");
        require(game.stake2 == 0, "Already joined");
        require(msg.value > 0, "Stake must be > 0");
        
        game.stake2 = msg.value;
        
        emit GameCreated(gameId, game.agent1, game.agent2, game.stake1, game.stake2);
    }
    
    /**
     * @dev Commit move using hash (commit-reveal pattern to prevent front-running)
     */
    function commitMove(uint256 gameId, bytes32 moveHash) external {
        Game storage game = games[gameId];
        require(game.stake2 > 0, "Game not ready");
        require(!game.settled, "Game already settled");
        require(msg.sender == game.agent1 || msg.sender == game.agent2, "Not a player");
        
        if (msg.sender == game.agent1) {
            require(!game.agent1Committed, "Already committed");
            game.agent1MoveHash = moveHash;
            game.agent1Committed = true;
        } else {
            require(!game.agent2Committed, "Already committed");
            game.agent2MoveHash = moveHash;
            game.agent2Committed = true;
        }
        
        emit MoveCommitted(gameId, msg.sender);
    }
    
    /**
     * @dev Reveal move and verify against hash
     */
    function revealMove(uint256 gameId, bool cooperate, string memory salt) external {
        Game storage game = games[gameId];
        require(game.agent1Committed && game.agent2Committed, "Moves not committed");
        require(!game.settled, "Game already settled");
        require(msg.sender == game.agent1 || msg.sender == game.agent2, "Not a player");
        
        bytes32 computedHash = keccak256(abi.encodePacked(cooperate, salt));
        
        if (msg.sender == game.agent1) {
            require(!game.agent1Revealed, "Already revealed");
            require(computedHash == game.agent1MoveHash, "Invalid reveal");
            game.agent1Cooperated = cooperate;
            game.agent1Revealed = true;
        } else {
            require(!game.agent2Revealed, "Already revealed");
            require(computedHash == game.agent2MoveHash, "Invalid reveal");
            game.agent2Cooperated = cooperate;
            game.agent2Revealed = true;
        }
        
        emit MoveRevealed(gameId, msg.sender, cooperate);
        
        // Auto-settle if both revealed
        if (game.agent1Revealed && game.agent2Revealed) {
            _settle(gameId);
        }
    }
    
    /**
     * @dev Settle the game and distribute payoffs based on Prisoner's Dilemma
     */
    function _settle(uint256 gameId) private {
        Game storage game = games[gameId];
        require(!game.settled, "Already settled");
        require(game.agent1Revealed && game.agent2Revealed, "Not ready to settle");
        
        game.settled = true;
        
        uint256 payout1;
        uint256 payout2;
        
        if (game.agent1Cooperated && game.agent2Cooperated) {
            // Both cooperate: (3, 3) - each gets 1.5x stake
            payout1 = (game.stake1 * BOTH_COOPERATE) / SCALE;
            payout2 = (game.stake2 * BOTH_COOPERATE) / SCALE;
        } else if (!game.agent1Cooperated && !game.agent2Cooperated) {
            // Both defect: (1, 1) - each gets 0.5x stake
            payout1 = (game.stake1 * BOTH_DEFECT) / SCALE;
            payout2 = (game.stake2 * BOTH_DEFECT) / SCALE;
        } else if (!game.agent1Cooperated && game.agent2Cooperated) {
            // Agent1 defects, Agent2 cooperates: (5, 0)
            payout1 = (game.stake1 * DEFECTOR_WINS) / SCALE;
            payout2 = (game.stake2 * COOPERATOR_LOSES) / SCALE;
        } else {
            // Agent1 cooperates, Agent2 defects: (0, 5)
            payout1 = (game.stake1 * COOPERATOR_LOSES) / SCALE;
            payout2 = (game.stake2 * DEFECTOR_WINS) / SCALE;
        }
        
        emit GameSettled(gameId, game.agent1, game.agent2, 
                        game.agent1Cooperated, game.agent2Cooperated, payout1, payout2);
        
        // Transfer payouts
        if (payout1 > 0) {
            payable(game.agent1).transfer(payout1);
        }
        if (payout2 > 0) {
            payable(game.agent2).transfer(payout2);
        }
    }
    
    /**
     * @dev Get game details
     */
    function getGame(uint256 gameId) external view returns (Game memory) {
        return games[gameId];
    }
    
    /**
     * @dev Timeout mechanism - if one player doesn't reveal, other can claim after timeout
     */
    function claimTimeout(uint256 gameId) external {
        Game storage game = games[gameId];
        require(!game.settled, "Already settled");
        require(block.timestamp > game.createdAt + 1 hours, "Timeout not reached");
        require(msg.sender == game.agent1 || msg.sender == game.agent2, "Not a player");
        
        game.settled = true;
        
        // If one revealed and other didn't, revealed player wins all
        if (game.agent1Revealed && !game.agent2Revealed) {
            uint256 totalPot = game.stake1 + game.stake2;
            payable(game.agent1).transfer(totalPot);
            emit GameSettled(gameId, game.agent1, game.agent2, game.agent1Cooperated, false, totalPot, 0);
        } else if (game.agent2Revealed && !game.agent1Revealed) {
            uint256 totalPot = game.stake1 + game.stake2;
            payable(game.agent2).transfer(totalPot);
            emit GameSettled(gameId, game.agent1, game.agent2, false, game.agent2Cooperated, 0, totalPot);
        } else {
            // Both failed to reveal, return stakes
            payable(game.agent1).transfer(game.stake1);
            payable(game.agent2).transfer(game.stake2);
            emit GameSettled(gameId, game.agent1, game.agent2, false, false, game.stake1, game.stake2);
        }
    }
}
